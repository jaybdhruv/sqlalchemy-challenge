# Import Dependencies
import numpy as np
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Define homepage route and list all the available routes
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query to get recent date
    recent_date_query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = str(recent_date_query)
    
    # Query to retrieve previous year's date from the recent date
    previous_year_date = datetime.strptime(recent_date[2:-3], '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query Date and Precipitation values for that one year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year_date).\
            order_by(Measurement.date).all()
    
    session.close()

    # Create a dictionary from row data where date is key and precipitation is value
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

# Define station route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query Station Names
    results = session.query(Station.name).all()

    session.close()

    station_names = list(np.ravel(results))
    return jsonify(station_names)

# Define temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    
    # Query to get recent date
    recent_date_query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = str(recent_date_query)
    
    # Query to retrieve previous year's date from the recent date
    previous_year_date = datetime.strptime(recent_date[2:-3], '%Y-%m-%d') - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= previous_year_date, Measurement.station == most_active_station[0]).all()
    
    session.close()

    tobs = list(np.ravel(results))
    return jsonify(tobs)

# Define start date route
@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start_date = datetime.strptime(start, '%Y-%m-%d')
    # 
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    session.close()

    temp_start = list(np.ravel(results))
    return jsonify(temp_start)

# Define start and end date route
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    # 
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    session.close()

    temp_start_end = list(np.ravel(results))
    return jsonify(temp_start_end)


if __name__ == "__main__":
    app.run(debug=True)
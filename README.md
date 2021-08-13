# SQLAlchemy-Challenge Readme

In this challenge, I've done climate analysis of Honolulu, Hawaii with data available from 2010-01-01 till 2017-08-23

## Step 1 - Climate Analysis and Exploration

To begin, I used Python and SQLAlchemy to do basic climate analysis and data exploration of my climate database. All of the following analysis were completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Used SQLAlchemy `create_engine` to connect to sqlite database.

* Used SQLAlchemy `automap_base()` to reflect tables into classes and save a reference to those classes called `Station` and `Measurement`.

* Linked Python to the database by creating an SQLAlchemy session.


### Precipitation Analysis

* Found the most recent date in the data set.

* Using this date, retrieved the last 12 months of precipitation data by querying the 12 preceding months of data.

* Selected only the `date` and `prcp` values.

* Loaded the query results into a Pandas DataFrame and set the index to the date column.

* Sorted the DataFrame values by `date`.

* Plotted the results using the DataFrame `plot` method.

* Used Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Designed a query to calculate the total number of stations in the dataset.

* Designed a query to find the most active stations (i.e. which stations have the most rows?).

  * Listed the stations and observation counts in descending order.

  * Listed station id that has the highest number of observations

  * Using the most active station id, calculated the lowest, highest, and average temperature using function such as `func.min`, `func.max`, `func.avg`, and `func.count` in my queries.

* Designed a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filtered by the station with the highest number of observations.

  * Query the last 12 months of temperature observation data for this station.

  * Plot the results as a histogram with `bins=12`.

* Graphs for both analysis are stored in Images folder in the repo

- - -

## Step 2 - Climate App

After completing my initial analysis, designed a Flask API based on the queries that I had just developed.

* Used Flask to create your routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.

  * Return a JSON representation of your dictionary of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  * Return a JSON representation of your dictionary of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

<h2>Temperature Analysis</h2>

I also used unpaired t-test to see if there is a meaningful difference between the temperature in, for example, June and December.

My analysis and related jupyter notebook is available in repo.

# Module10

OVERVIEW
This code contatins two primary files: a jupyter notebook - climate_starter.ipynb & a python file - app.py. Both of these files run query's on a sqlite databse named hawaii.sqlite. 

CLIMATE STARTER
In this file we start by creating an engine to access a sqlite database, which consists of two tables measurement and station. In the exploratory precipitation analysis we find the most recent date in the data and query to retrieve the precipitation data from the last year. I then plot that data using pandas and matplotlib and generate summary statistics on it. In the exploratory station analysis i count the number of stations, find the most active station, and run temperature calculations for the most active station. Finallly a generate a histogram for this data. 

App.py
This code is a Flask API that provides data about precipitation, stations, and temperature in Hawaii. The data is retrieved from a SQLite database.

The API will be available at http://localhost:5000/.

The following API endpoints are available:

/api/v1.0/precipitation
Returns a list of precipitation data for the past year.
/api/v1.0/stations
Returns a list of all stations.
/api/v1.0/tobs
Returns a list of temperature data for the most active station in the past year.
/api/v1.0/<start>
Returns the minimum, average, and maximum temperature for all dates after start.
/api/v1.0/<start>/<end>
Returns the minimum, average, and maximum temperature for all dates between start and end.

I completed this homework assignment using class resources other internet resources 

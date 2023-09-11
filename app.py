# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
from flask import Flask, jsonify
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/antho/Documents/Coding_bootcamp/Projects/Modeule 10/Starter_Code/Resources\hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#API Info
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
        f"Note The Date Format is YYYY-MM-DD"
    )

#Precipitation API#
@app.route("/api/v1.0/precipitation")

#Function that recalls percipitation data into a dictionary 
def precipitation():
    #Query to call date and percipitation data from measurement table
    results = session.query(measurement.date, measurement.prcp).all()

    #List to store all precipitation data
    all_precipitation = []

    #Storing precipitation data in a dicitionary
    for date, prcp in results:
        precipitation_dictionary = {}
        precipitation_dictionary["date"] = date
        precipitation_dictionary["prcp"] = prcp
        all_precipitation.append(precipitation_dictionary)

    #Return the list data
    return jsonify(all_precipitation)

#Stations API# 
@app.route("/api/v1.0/stations")

#Function that recalls all station data
def stations():
    #Query to call station data
    results = session.query(station.station).all()
    #list to store all results data
    all_stations = list(np.ravel(results))
    #Return the list data 
    return jsonify(all_stations)

#Temperature API# 
@app.route("/api/v1.0/tobs")

#Funtion that recalls all temperature data 
def tobs():
    #Find last date in the measurement table 
    raw_last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    #Convert that to a date
    last_date = datetime.strptime(raw_last_date[0], '%Y-%m-%d')
    #Date one year prior 
    one_year_ago = last_date - timedelta(days=365)

    #Query to find most active station
    most_active=session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    ma_results = session.query(measurement.date, measurement.tobs).filter((measurement.station == most_active[0][0]) & (measurement.date >= one_year_ago)).all()

    # Convert results to a list
    tobs_list = []
    for date, temp in ma_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = temp
        tobs_list.append(tobs_dict)
    
    #Return list data 
    return jsonify(tobs_list)

#API Functionality to run calculations on the data available starting at the entered date
@app.route("/api/v1.0/<start>")
#Function that makes calculations on temperature 
def calc_temp_start(start):
    #Query to pull measurement data 
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    #Create a dictionary to store data
    temp_dict_start = {}
    #Store min, avg, and max data 
    temp_dict_start["Min_Temp"] = results[0][0]
    temp_dict_start["Avg_Temp"] = results[0][1]
    temp_dict_start["Max_Temp"] = results[0][2]
    #Return dictionary data 
    return jsonify(temp_dict_start)

#API functionality to calculate the temperature data with a start & end date 
@app.route("/api/v1.0/<start>/<end>")
#Function that takes in start & end date to run calculation
def calc_temp_all(start, end):
    #Query the measurement data & perform calculations
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    #Dictionary to store data 
    temp_dict_all = {}
    temp_dict_all["Min_Temp"] = results[0][0]
    temp_dict_all["Avg_Temp"] = results[0][1]
    temp_dict_all["Max_Temp"] = results[0][2]
    return jsonify(temp_dict_all)


if __name__ == '__main__':
    app.run(debug=True)
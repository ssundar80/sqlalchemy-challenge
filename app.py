############################################### 
# Import Modules
###############################################
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Create a Secret Key
app.config['Secret Key'] = '6d2808e6627a23651c546c7b78b7c02f'
#################################################

# 1. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return '''Welcome to my app! 
           <br /> Available Routes: 
           <br /> 1) /api/v1.0/precipitation
           <br /> 2) /api/v1.0/stations
           <br /> 3) /api/v1.0/tobs
           <br /> 4) /api/v1.0/&ltstart&gt  
           <br /> 5) /api/v1.0/&ltstart&gt/&ltend&gt'''


# 2. Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session
    session= Session(engine)

    #Query Measurement Table
    precipt = session.query(Measurement.date, Measurement.prcp).all()

    #Close session
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipt = []
    for date, prcp in precipt:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_precipt.append(prcp_dict)

    return jsonify(all_precipt)

# 3. Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    #Create session
    session= Session(engine)

    #Query all station
    station = session.query(Station.station).all()

    #Close session
    session.close()

    #Convert list of tuples into normal list
    all_stations = list(np.ravel(station))

    return jsonify(all_stations)

# 4. Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
     #Create session
     session= Session(engine)
     
     #Query for the dates and temperature observations from a year from the last data point
     obj = session.query(Measurement).order_by(Measurement.date.desc()).first()
     dates = [obj.date]   
     l = [d.date() for d in pd.to_datetime(dates)]
     past_year= l[0] - timedelta(days = 365)
     temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= past_year).all()

     #Close session
     session.close()

     #Convert list of tuples into normal list
     all_temp = list(np.ravel(temp))
     return jsonify(all_temp)

# 5. Define what to do when a user hits the /api/v1.0/<start> route

@app.route("/api/v1.0/<start>")
def departure():

    #Create session
    session= Session(engine)

    #Create input for start date
    "Enter your trip start date (DD/MM/YYYY)"
    start_date = input("What is your date of departure?")

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    #Close session
    session.close()
    
    return jsonify(result)
    
# 6. Define what to do when a user hits the /api/v1.0/<start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def start_end():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

if __name__ == "__main__":
    app.run(debug=True)
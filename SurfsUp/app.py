# Import the dependencies.
import numpy as np
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station


# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)







#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2014-08-03<br/>"
        f"Enter date in format of YYYY-MM-DD between 2010-01-01 and 2017-08-23<br/>"
        f"/api/v1.0/2013-06-08/2017-01-28<br/>"
        f"Enter date in format of YYYY-MM-DD between 2010-01-01 and 2017-08-23"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.

    year_range = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    query = session.query(Measurement.date, Measurement.prcp).\
                                filter(Measurement.date >= year_range).all()

    #convert query into dictionary
    climate_dict = [{'Date': date, 'precipitation': prcp} for date, prcp in query]

    #return Json file
    return jsonify(climate_dict)

@app.route("/api/v1.0/stations")
def stations():
    # query to find stations
    query_station= session.query(Measurement.station).group_by(Measurement.station).all()
  
    #convert query into dictionary
    
    station_names = list(np.ravel(query_station))

    #return Json file of stations
    return jsonify(station_names)   

@app.route("/api/v1.0/tobs")
def tobs():
    #defining the last year range
    year_range = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #perform query to find date and temperature readings for previous year
    year_temp_query=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').\
                                            filter(Measurement.date >= year_range).all()
    
    #convert query into dictionary
    temp_dict = [{'Date': date, 'Temperature': temp} for date, temp in year_temp_query]

    #return Json file
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>")
def temp_data(start):
    #defining variables
    start_date=start
    #perform query to find min, max and av temperatures
    station_temp=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
        
    #convert query into dictionary
    temp_dict = [{'Min Temperature': min, 'Max Temperature': max, 'Average Temperature': avg} for min, max, avg in station_temp]
    # return Json file
    return jsonify(temp_dict)
        
@app.route("/api/v1.0/<start>/<end>")
def range_temp(start,end):
    #defining variables
    start_date=start
    end_date=end
    #perform query to find min, max and av temperatures
    station_temp=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        
    #convert query into dictionary
    temp_dict = [{'Min Temperature': min, 'Max Temperature': max, 'Average Temperature': avg} for min, max, avg in station_temp]
    # return Json file
    return jsonify(temp_dict)
        

if __name__ == "__main__":
    app.run(debug=True)


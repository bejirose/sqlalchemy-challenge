import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request, escape


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    start = "/api/v1.0/" + escape("<start>")
    start_end = "/api/v1.0/" + escape("<start>/<end>")
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"{start}<br/>"
        f"{start_end}<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """query precipitation for last year"""
    # 
    ld = engine.execute("SELECT strftime('%Y-%m-%d', max(Measurement.date), '-1 years') from Measurement").fetchall()
    last_year = ld[0][0]

    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, func.round(func.avg(Measurement.prcp),2)).filter(Measurement.date >= \
                                last_year).group_by(Measurement.date).order_by(Measurement.date).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

#list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all station names
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

# Find dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Choose the station with the highest number of temperature observations.
    highest_station = session.query(Measurement.station).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    
    # find the latest date available for this stations
    tob_date = session.query(Measurement.date).filter(Measurement.station == highest_station[0]).order_by(Measurement.date.desc()).first()[0]

    # find the 12 months back date
    tobs_last_year = dt.datetime.strptime(tob_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the last 12 months of date and temperature observation data for this station
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= tobs_last_year).\
        filter(Measurement.station == highest_station[0]).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# calculate the TMIN, TAVG, and TMAX for the given date or a date greater than or equal to the start date
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    # calculate the TMIN, TAVG, and TMAX for a date greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))
    return jsonify(tobs_list)
    
# calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)

# -*- coding: utf-8 -*-
"""
Created on Sun May 10 09:48:21 2020

@author: gshre
"""

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import json

import datetime as dt
import numpy as np
from dateutil.relativedelta import relativedelta

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#shared constant
last_day_of_data_dt = dt.date(2017,8,23)

class Precipitation():
    
    def __init__(self, date, prcp):
        self.date = date
        self.prcp = prcp;
        
    def serialize(self):
        return {
            "date": self.date,
            "prcp": self.prcp
            }

def get_12_months_back_date():
    twelve_months_delta = relativedelta(months=12)
    one_year_ago_date = last_day_of_data_dt - twelve_months_delta
    return one_year_ago_date

    
def get_most_active_station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel=[Station.station,
        func.count(Measurement.tobs)]
    
    one_year_ago_date = get_12_months_back_date()
    
    active_stations_query = session.query(*sel).filter(Measurement.station == Station.station) \
            .filter(Measurement.date >= one_year_ago_date).group_by(Station.station) \
            .filter(Measurement.tobs != None) \
            .order_by(func.count(Measurement.tobs).desc())
    return active_stations_query.limit(1)[0][0]    


def get_precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
  
    # Perform a query to retrieve the data and precipitation scores
    prcp_data = session.query(Measurement.date, Measurement.prcp) \
       .all()
       
    prcps = list(np.ravel(prcp_data))
        
    return {"precipitations": prcps}
 

def get_stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Save references to each table
    Station = Base.classes.station
  
    # Perform a query to retrieve the data and precipitation scores
    station_data = session.query(Station).all()
    
    stations = []
    for station in station_data:
        # stations.append(station.__dict__)
        stations.append({"id": station.id,
                          "station": station.station,
                          "name" : station.name,
                          "latitude" : station.latitude,
                          "longitude" : station.longitude,
                          "elevation": station.elevation})
        
    return stations   

def get_most_active_station_temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    
    most_active_station = get_most_active_station()
    one_year_ago_date = get_12_months_back_date()
    
    last_12_months_temp = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.station == Station.station) \
        .filter(Measurement.date >= one_year_ago_date) \
        .filter(Measurement.station == most_active_station).all()

    tobs_list = []
    for date, tobs in last_12_months_temp:
        tobs_list.append({"date": date, "tobs": tobs})
    return {"most_active_station": most_active_station,
            "tobs_list": tobs_list}

def get_temperatures_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Save references to each table
    Measurement = Base.classes.measurement
    
    sel=[func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)]
   
    if end == None:
        query = session.query(*sel).filter(Measurement.date >= start)
    else:
        query = session.query(*sel).filter(Measurement.date >= start) \
            .filter(Measurement.date <= end)

    statistics_data = query.all()
    print(statistics_data)
    
    # Verify that data was found for the time range
    if statistics_data[0][0] != None:  
        result = {"start": start,
                  "tmin" : statistics_data[0][0],
                  "tmax" : statistics_data[0][1],
                  "tavg" : round(statistics_data[0][2], 1),
                  }
    else:
        result = {"start": start,
                  "result": "No data found"
                  }
    # end is not always provided, so only show when provided
    if end != None:
        result["end"] = end
    
    return result
#tobs = get_most_active_station_temperatures()

#most_active_station = get_most_active_station()        
    
# stations = get_stations()
# print(stations)

#precipitations = get_precipitations()
#print(precipitations)
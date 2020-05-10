# -*- coding: utf-8 -*-
"""
Created on Sat May  9 11:42:43 2020

@author: gshreve
"""

from flask import Flask
import json

from hawaii_orm import Precipitation, get_precipitations, get_stations, \
    get_most_active_station_temperatures

app = Flask(__name__)


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    # return a result that describes the api 
    html_response = "The following api requests are supported:</p>" + \
            "/api/v1.0/precipitation</br>" + \
            "/api/v1.0/stations</br>" + \
            "/api/v1.0/tobs</br>" + \
            "/api/v1.0/&lt;start&gt; and /api/v1.0/&lt;start&gt;/&lt;end&gt;" 
    return html_response



# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcps = get_precipitations()
    dic_list = [prcp.serialize() for prcp in prcps]
    json_rep = json.dumps(dic_list)    
    print("Server received request for 'precipitations' api...")
    return json.dumps(dic_list) 

@app.route("/api/v1.0/stations")
def stations():
    stations = get_stations()
    print("Server received request for 'stations' api...")
    return json.dumps(stations) 

@app.route("/api/v1.0/tobs")
def most_active_station_temperatures():
    tobs = get_most_active_station_temperatures()
    print("Server received request for 'tobs' api...")
    return json.dumps(tobs) 

if __name__ == "__main__":
    app.run(debug=True)


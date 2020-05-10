# -*- coding: utf-8 -*-
"""
Created on Sat May  9 11:42:43 2020

@author: gshreve
"""

from flask import Flask, jsonify
import json
import datetime as dt
import sys

from hawaii_orm import Precipitation, get_precipitations, get_stations, \
    get_most_active_station_temperatures, get_temperatures_start_end

app = Flask(__name__)

def is_valid_date(date_string):
    date_format = "%Y-%m-%d"
    try:
        date_obj = dt.datetime.strptime(date_string, date_format)
        return True
    except:
        e = sys.exc_info()[0]
        print("<p>Error: %s</p>" % e )
        return False


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
    #dic_list = [prcp.serialize() for prcp in prcps]
    #json_rep = json.dumps(dic_list)    
    print("Server received request for 'precipitations' api...")
    return jsonify(prcps) 

@app.route("/api/v1.0/stations")
def stations():
    stations = get_stations()
    print("Server received request for 'stations' api...")
    return jsonify(stations) 

@app.route("/api/v1.0/tobs")
def most_active_station_temperatures():
    tobs = get_most_active_station_temperatures()
    print("Server received request for 'tobs' api...")
    return jsonify(tobs) 


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def get_temperatures_start(start,end=None):
    if not is_valid_date(start):
        return jsonify({"error": f"Provided value for start is not in valid date format [{start}].  Please provide date in 'YYYY-MM-DD' format."}), 404
    if end != None and not is_valid_date(end):
        return jsonify({"error": f"Provided value for end is not in valid date format [{start}].  Please provide date in 'YYYY-MM-DD' format."}), 404
    if end != None and end < start:
        return jsonify({"error": f"Provided end value is less than the start value: start=[{start}] end=[{start}].  End date cannot be less than the start date."}), 404
        
    temps = get_temperatures_start_end(start, end)
    print("Server received request for '<start>/<end>' api...")
    return jsonify(temps) 


if __name__ == "__main__":
    app.run(debug=True)


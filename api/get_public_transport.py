from flask import Flask
from flask import request
import requests
import json
import math
import sqlite3
from mapbox_api import getRouteInfo

app = Flask(__name__)

@app.route('/getPublicTransport', methods = ['POST'])
def getPublicTransport():
    # Latitude --> 1 deg = 110.574 km
    # Longitude --> 1 deg = 111.320*cos(latitude in radians) km
    return request.form
    maxDistance = 1
    radiusIncrement = 1
    pi = 22/7
    cityLat = 28.6
    # input
    sourceLat = 0
    sourceLong = 0
    destLat = 0
    destLong = 0
    # get this data from db
    db = get_db()
    d.execute(
        'SELECT * FROM bus_shelters;'
    ).fetchall()
    metroLocations = []
    nearestMetroLocationsToSource = []
    nearestMetroLocationsToDest = []

    # calculate distance of each metro station from source
    # this would be inclusive of auto stands/bus stands, all maybe distinguished by a field in each row
    while maxDistance < 10:
        for metro in metroLocations:
            distance = pow((pow((metro.lat-sourceLat)*110.574, 2) + pow((metro.long-sourceLong)*111.320*math.cos(cityLat/180*pi), 2)), 0.5)
            if distance < maxDistance:
                nearestMetroLocationsToSource.append(metro)
        maxDistance = maxDistance + radiusIncrement

    maxDistance = 1
    # repeat for destination
    while maxDistance < 10:
        for metro in metroLocations:
            distance = pow((pow((metro.lat-destLat)*110.574, 2) + pow((metro.long-destLong)*111.320*math.cos(cityLat/180*pi), 2)), 0.5)
            if distance < maxDistance:
                nearestMetroLocationsToDest.append(metro)
        maxDistance = maxDistance + radiusIncrement

    # time taken if no public transport is considered - straight from source to dest
    # get from API
    directRoute = getRouteInfo(sourceLat, sourceLong, destLat, destLong)
    directTime = directRoute.routes[0].duration
    directDistance = directRoute.routes[0].distance

    for sourceMetro in nearestMetroLocationsToSource:
        routeFromSourceToMetro = getRouteInfo(sourceLat, sourceLong, sourceMetro.latitude, sourceMetro.longitude)
        timeFromSourceToMetro = directRoute.routes[0].duration
        # if time from source to metro itself exceeds direct pathing time, remove
        if timeFromSourceToMetro > directTime:
            nearestMetroLocationsToSource.remove(sourceMetro)

    # similarly for destination
    for destMetro in nearestMetroLocationsToDest:
        routeFromMetroToDest = getRouteInfo(destMetro.latitude, destMetro.longitude, destLat, destLong)
        timeFromMetroToDest = directRoute.routes[0].duration
        # if time from source to metro itself exceeds direct pathing time, remove
        if timeFromMetroToDest > directTime:
            nearestMetroLocationsToSource.remove(destMetro)

if __name__ == '__main__':
   app.run()

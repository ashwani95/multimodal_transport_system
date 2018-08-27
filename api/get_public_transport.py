from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import math
import sqlite3
from mapbox_api import getRouteInfo
from distance_matrix_api import getDitanceAndTime
from config import UBER_API_KEY


def getFastestRoute(sourceLat, sourceLong, destLat, destLong):
    print(sourceLat)
    return sourceLat
    nearestMetroLocationsToSource, nearestMetroLocationsToDest = getPublicTransport(sourceLat, sourceLong, destLat, destLong)
    totalJourneyTime = math.inf
    sourceDestMetroCombo = []
    for sourceMetro in nearestMetroLocationsToSource:
        for destMetro in nearestMetroLocationsToDest:
            # this must take into account the waiting time according the next train/metro's arrival
            # routeInfo = getTotalJourneyTime(sourceLat, sourceLong, destLat, destLong, sourceMetro, destMetro)
            # if routeInfo['time'] < totalJourneyTime:
            #     totalJourneyTime = routeInfo['time']
            #     sourceDestMetroCombo['source'] = sourceMetro
            #     sourceDestMetroCombo['dest'] = destMetro
            totalRouteDetails = getTotalJourneyTime(sourceLat, sourceLong, destLat, destLong, sourceMetro, destMetro)
            # if totalRouteTime < totalJourneyTime:
            # totalJourneyTime = totalRouteTime
            sourceDestMetroCombo['source'] = sourceMetro
            sourceDestMetroCombo['dest'] = destMetro
            sourceDestMetroCombo['time'] = totalRouteDetails
            sourceDestMetroCombo['price'] = totalRouteDetails

    return nearestMetroLocationsToSource, nearestMetroLocationsToDest


def getPublicTransport(sourceLat, sourceLong, destLat, destLong):
    # Latitude --> 1 deg = 110.574 km
    # Longitude --> 1 deg = 111.320*cos(latitude in radians) km
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
        'SELECT * FROM public_coordinates;'
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
                # metro.distance = distance
                nearestMetroLocationsToSource.append(metro)
        maxDistance = maxDistance + radiusIncrement

    maxDistance = 1
    # repeat for destination
    while maxDistance < 10:
        for metro in metroLocations:
            distance = pow((pow((metro.lat-destLat)*110.574, 2) + pow((metro.long-destLong)*111.320*math.cos(cityLat/180*pi), 2)), 0.5)
            if distance < maxDistance:
                # metro.distance = distance
                nearestMetroLocationsToDest.append(metro)
        maxDistance = maxDistance + radiusIncrement

    # time taken if no public transport is considered - straight from source to dest
    # get from API
    directRoute = getRouteInfo(sourceLat, sourceLong, destLat, destLong)
    directTime = directRoute.routes[0].duration
    directDistance = directRoute.routes[0].distance

    for sourceMetro in nearestMetroLocationsToSource:
        routeFromSourceToMetro = getRouteInfo(sourceLat, sourceLong, sourceMetro.latitude, sourceMetro.longitude)
        timeFromSourceToMetro = routeFromSourceToMetro.routes[0].duration
        # if time from source to metro itself exceeds direct pathing time, remove
        if timeFromSourceToMetro > directTime:
            nearestMetroLocationsToSource.remove(sourceMetro)

    # similarly for destination
    for destMetro in nearestMetroLocationsToDest:
        routeFromMetroToDest = getRouteInfo(destMetro.latitude, destMetro.longitude, destLat, destLong)
        timeFromMetroToDest = routeFromMetroToDest.routes[0].duration
        # if time from source to metro itself exceeds direct pathing time, remove
        if timeFromMetroToDest > directTime:
            nearestMetroLocationsToSource.remove(destMetro)

    return nearestMetroLocationsToSource, nearestMetroLocationsToDest


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def getTotalJourneyTime(sourceLat, sourceLong, destLat, destLong, sourceMetro, destMetro):
    # Step 1 - get time taken from source to sourceMetro
    uberApiURL = "https://api.uber.com/v1.2/estimates/price"
    uberQueryString = {
        "start_latitude": sourceLat,
        "start_longitude": sourceLong,
        "end_latitude": destLat,
        "end_longitude": destLong
    }
    uberHeaders = {
        'Authorization': "Token " + UBER_API_KEY,
        'Accept-Language': "en_US",
        'Content-Type': "application/json"
    }
    firstLeg = requests.request("GET", uberApiURL, headers=uberHeaders, params=uberQueryString)
    firstLegTime = firstLeg['prices'][0]['duration']
    firstLegPrice = firstLeg['prices'][0]['estimate']
    # Step 2 - get next ETA for bus/metro from that station

    # Step 3 - time taken to travel from sourceMetro to destMetro
    # Step 4 - time taken to travel from destMetro to dest
    # Step 5 - add all times, including the waiting time
    return ''

# getFastestRoute(28.2, 77.2, 28.5, 77.6)

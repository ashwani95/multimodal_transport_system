import os

from flask import Flask
from flask import jsonify
import math
import sqlite3
from config import MAP_BOX_API_KEY
import requests

def create_app(test_config=None):

    app=Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'multi-modal.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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

    @app.route('/getRouteInfo')
    def getRouteInfo(sourceLat, sourceLong, destLat, destLong):
        r = requests.get('https://api.mapbox.com/directions/v5/mapbox/driving-traffic/' + sourceLat + ',' +
                         sourceLong + ';' + destLat + ',' + destLong + '?access_token='+MAP_BOX_API_KEY+'&steps=true')
        apiResponse = jsonify(r.json())
        return apiResponse
        # return 'Total time: ' + apiResponse.routes[0].duration + ' Total distance: ' + apiResponse.routes[0].distance

    @app.route('/getPublicTransport')
    def getPublicTransport():
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
            'SELECT * FROM bus_shelters;'
        ).fetchall()
        metroLocations = []
        nearestMetroLocationsToSource = []
        nearestMetroLocationsToDest = []

        # calculate distance of each metro station distance from source
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

    return app
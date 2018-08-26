import os

from flask import Flask
from flask import jsonify
from flask import json
import sqlite3

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

    @app.route('/hello')
    def hello():
        return 'Whatssup!!!'

    @app.route('/getData')
    def getData():
        r = requests.get('https://api.mapbox.com/directions/v5/mapbox/driving-traffic/-122.42,37.78;-77.03,38.91?access_token=pk.eyJ1IjoiYnVja3MiLCJhIjoiY2psOWh4NWZjM3R0dDNwbnNyMHVhcm54aiJ9.w4kFjaIepPoSGg7vueYP9g&steps=true')
        apiResponse = jsonify(r.json())
        return apiResponse
        # return 'Total time: ' + apiResponse.routes[0].duration + ' Total distance: ' + apiResponse.routes[0].distance

    @app.route('/getPublicTransport')
    def getPublicTransport():


    return app
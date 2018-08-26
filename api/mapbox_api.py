import os

from flask import Flask
from flask import jsonify
from api.config import MAP_BOX_API_KEY
import requests
import json

app = Flask(__name__)

def getRouteInfo(sourceLat, sourceLong, destLat, destLong):
    url = 'https://api.mapbox.com/directions/v5/mapbox/driving-traffic/' + sourceLat + ',' + sourceLong + ';' + destLat + ',' + destLong
    queryString = {
        'access_token': MAP_BOX_API_KEY,
        'steps': 'true'
    }
    apiResponse = requests.request('GET', url, params=queryString)
    jsonResponse = apiResponse.json()
    result = {"distance": jsonResponse['routes'][0]['distance'], "time": jsonResponse['routes'][0]['duration']}
    return json.dumps(result)

if __name__ == '__main__':
   app.run()

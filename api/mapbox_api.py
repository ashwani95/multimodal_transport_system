import os

from flask import Flask
from flask import jsonify
from config import MAP_BOX_API_KEY
import requests

app = Flask(__name__)

@app.route('/getRouteInfo')
def getRouteInfo(sourceLat, sourceLong, destLat, destLong):
    r = requests.get('https://api.mapbox.com/directions/v5/mapbox/driving-traffic/' + sourceLat + ',' +
                     sourceLong + ';' + destLat + ',' + destLong + '?access_token='+MAP_BOX_API_KEY+'&steps=true')
    apiResponse = jsonify(r.json())
    return apiResponse
    # return 'Total time: ' + apiResponse.routes[0].duration + ' Total distance: ' + apiResponse.routes[0].distance

if __name__ == '__main__':
   app.run()

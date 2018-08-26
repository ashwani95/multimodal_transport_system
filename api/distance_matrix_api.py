from flask import Flask
import requests
import json
from config import DISTANCE_MATRIX_API_KEY

url = "https://maps.googleapis.com/maps/api/distancematrix/json"
API_KEY=DISTANCE_MATRIX_API_KEY

headers = {'Cache-Control': "no-cache"}


app = Flask(__name__)

@app.route('/getDistanceMatrixData')
def getDitanceAndTime():
    origin = "12.981936, 77.645324"
    destination = "12.965835, 77.647083"
    querystring = {"units": "metric", "origins": origin, "destinations": destination, "key": API_KEY}
    response = requests.request("GET", url, headers=headers, params=querystring)
    distance,time = parseResponse(response.json())
    result = {"distance":distance,"time":time}
    return json.dumps(result)


def parseResponse(response):
    element = response["rows"][0]["elements"][0]
    distance = element["distance"]["text"]
    time = element["duration"]["text"]

    return distance,time


if __name__ == '__main__':
   app.run()


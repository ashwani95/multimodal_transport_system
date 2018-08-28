from flask import Flask
import requests
import json
from config import DISTANCE_MATRIX_API_KEY

url = "https://maps.googleapis.com/maps/api/distancematrix/json"
API_KEY=DISTANCE_MATRIX_API_KEY

headers = {'Cache-Control': "no-cache"}


def getDistanceAndTime(sourceLat, sourceLong, destLat, destLong):
    origin = str(sourceLat) + ", " + str(sourceLong)
    destination = str(destLat) + ", " + str(destLong)
    querystring = {"units": "metric", "origins": origin, "destinations": destination, "key": API_KEY}
    response = requests.request("GET", url, headers=headers, params=querystring)
    distance,time = parseResponse(response.json())
    result = {"distance":distance,"time":time}
    return result


def parseResponse(response):
    element = response["rows"][0]["elements"][0]
    distance = element["distance"]["text"]
    time = element["duration"]["text"]

    return distance,time

from flask import Flask
import requests
import json
from config import DISTANCE_MATRIX_API_KEY

url = "https://maps.googleapis.com/maps/api/distancematrix/json"
API_KEY=DISTANCE_MATRIX_API_KEY

headers = {'Cache-Control': "no-cache"}

def getDitanceAndTime(sourceLat,sourceLong,destLat,destLong):
    origin = str(sourceLat)+", "+str(sourceLong)
    destination = str(destLat)+", "+str(destLong)
    querystring = {"units": "metric", "origins": origin, "destinations": destination, "key": API_KEY}
    response = requests.request("GET", url, headers=headers, params=querystring)
    distance,time = parseResponse(response.json())
    result = {"distance":distance,"time":time}
    return json.dumps(result)


def parseResponse(response):
    element = response["rows"][0]["elements"][0]
    distance = element["distance"]["value"]
    time = element["duration"]["value"]

    return distance,time

print(getDitanceAndTime(28.637408, 77.217423, 28.642385, 77.206003))

from flask import Flask
import requests
import json

from api.config import DISTANCE_MATRIX_API_KEY

url = "https://maps.googleapis.com/maps/api/distancematrix/json"
API_KEY=DISTANCE_MATRIX_API_KEY

headers = {'Cache-Control': "no-cache"}


def getDistanceAndTime(sourceLat, sourceLong, destLat, destLong):
    origin = str(sourceLat) + ", " + str(sourceLong)
    destination = str(destLat) + ", " + str(destLong)
    querystring = {"units": "metric", "origins": origin, "destinations": destination, "key": API_KEY}
    response = requests.request("GET", url, headers=headers, params=querystring)
    distance_value,distance_text,time_value,time_text = parseResponse(response.json())
    result = {"distance_value":distance_value,"time_value":time_value,"distance_text":distance_text,"time_text":time_text}
    return json.dumps(result)


def parseResponse(response):
    element = response["rows"][0]["elements"][0]
    distance_value = element["distance"]["value"]
    distance_text = element["distance"]["text"]
    time_value = element["duration"]["value"]
    time_text = element["duration"]["text"]

    return distance_value,distance_text,time_value,time_text



#print(getDistanceAndTime(28.637408, 77.217423, 28.642385, 77.206003))



from api.config import MAP_BOX_API_KEY
import requests
import json


def getRouteInfo(sourceLat, sourceLong, destLat, destLong):
    url = 'https://api.mapbox.com/directions/v5/mapbox/driving-traffic/' + str(sourceLat) + ',' + str(sourceLong) + ';' + str(destLat) + ',' + str(destLong)
    queryString = {
        'access_token': MAP_BOX_API_KEY,
        'steps': 'true'
    }
    headers = {
        'Content-Type': "application/json"
    }
    apiResponse = requests.request("GET", url, headers=headers, params=queryString)
    jsonResponse = apiResponse.json()
    print(jsonResponse["message"])
    if(jsonResponse['routes'] is None):
        result = {"distance": 0, "time": 0}
    else:
        result = {"distance": jsonResponse['routes'][0]['distance'], "time": jsonResponse['routes'][0]['duration']}
    return json.dumps(result)

# getRouteInfo(28.2, 77.2, 28.5, 77.6)

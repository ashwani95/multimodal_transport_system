import requests
import json
import math
import csv
# from mapbox_api import getRouteInfo
from distance_matrix_api import getDistanceAndTime
from config import UBER_API_KEY
import time

# db = _mysql.connect("localhost", "root", "", "commute")


def getFastestRoute(sourceLat, sourceLong, destLat, destLong):
    nearestMetroLocationsToSource, nearestMetroLocationsToDest = getPublicTransport(sourceLat, sourceLong, destLat, destLong)
    totalJourneyTime = math.inf
    allSourceDestCombos = []
    sourceDestMetroCombo = []
    breakOutOfLoop = False
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
            # sourceDestMetroCombo['source'] = sourceMetro
            # sourceDestMetroCombo['dest'] = destMetro
            # sourceDestMetroCombo['time'] = totalRouteDetails["totalTime"]
            # sourceDestMetroCombo['price'] = totalRouteDetails["totalPrice"]
            if totalRouteDetails["isSourceCab"] is True and totalRouteDetails["isDestCab"] is True:
                sourceDestMetroCombo = {
                    'source': sourceMetro,
                    'dest': destMetro,
                    'totalTime': totalRouteDetails["totalTime"],
                    'totalPrice': totalRouteDetails["totalPrice"],
                    'otherDetails': totalRouteDetails
                }
                allSourceDestCombos.append(sourceDestMetroCombo)
                breakOutOfLoop = True
                break
        if breakOutOfLoop is True:
            break

    response = {
        'message': 'Take cab till ' + str(allSourceDestCombos[0]['source']['stopname']) + ', take metro from ' + str(allSourceDestCombos[0]['source']['stopname']) + ' ,get down from metro at ' + str(allSourceDestCombos[0]['dest']['stopname']) + ', take cab till destination',
        'totalPrice': str(allSourceDestCombos[0]['totalPrice']),
        'priceBreakdown': [
            {
                'firstLeg': str(allSourceDestCombos[0]['otherDetails']['firstLegPrice'])
            },
            {
                'secondLeg': '25'
            },
            {
                'endLeg': str(allSourceDestCombos[0]['otherDetails']['endLegPrice'])
            }
        ]
    }
    return response


def getPublicTransport(sourceLat, sourceLong, destLat, destLong):
    # Latitude --> 1 deg = 110.574 km
    # Longitude --> 1 deg = 111.320*cos(latitude in radians) km
    maxDistance = 1
    radiusIncrement = 1
    pi = 22/7
    cityLat = 28.6
    metroLocations = []
    # **********************************************************************
    # **********************************************************************
    # **********************************************************************
    # **********************************************************************
    # get this data from db
    # db.query(
    #     'SELECT * FROM public_coordinates'
    # )
    # r = db.store_result()
    # metroLocations = r.fetch_row(0, 1)
    # **********************************************************************
    # **********************************************************************
    # **********************************************************************
    # **********************************************************************

    with open('resources/public_coordinates.csv', 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        for line in reader:
            metroLocations.append(line)

    nearestMetroLocationsToSource = []
    nearestMetroLocationsToDest = []

    # calculate distance of each metro station from source
    # this would be inclusive of auto stands/bus stands, all maybe distinguished by a field in each row
    sourceMetroFound = False
    while maxDistance < 10:
        for metro in metroLocations:
            # use when fetching from db
            # metroLat = float(metro['coordinates'].decode().split(", ")[0])
            # metroLong = float(metro['coordinates'].decode().split(", ")[1])
            metroLat = float(metro['coordinates'].split(", ")[0])
            metroLong = float(metro['coordinates'].split(", ")[1])
            distance = pow((pow((metroLat-sourceLat)*110.574, 2) + pow((metroLong-sourceLong)*111.320*math.cos(cityLat/180*pi), 2)), 0.5)
            if distance < maxDistance:
                sourceMetroFound = True
                metro["distance"] = distance
                nearestMetroLocationsToSource.append(metro)
        if sourceMetroFound:
            break
        maxDistance = maxDistance + radiusIncrement

    maxDistance = 1
    destMetroFound = False
    # repeat for destination
    while maxDistance < 10:
        for metro in metroLocations:
            # use when fetching from db
            # metroLat = float(metro['coordinates'].decode().split(", ")[0])
            # metroLong = float(metro['coordinates'].decode().split(", ")[1])
            metroLat = float(metro['coordinates'].split(", ")[0])
            metroLong = float(metro['coordinates'].split(", ")[1])
            distance = pow((pow((metroLat-destLat)*110.574, 2) + pow((metroLong-destLong)*111.320*math.cos(cityLat/180*pi), 2)), 0.5)
            if distance < maxDistance:
                destMetroFound = True
                metro["distance"] = distance
                nearestMetroLocationsToDest.append(metro)
        if destMetroFound:
            break
        maxDistance = maxDistance + radiusIncrement

    # time taken if no public transport is considered - straight from source to dest
    # get from API
    directRoute = json.loads(getDistanceAndTime(sourceLat, sourceLong, destLat, destLong))
    directTime = directRoute["time_value"]
    directDistance = directRoute["distance_value"]

    for sourceMetro in nearestMetroLocationsToSource:
        sourceMetroLat = float(sourceMetro['coordinates'].split(", ")[0])
        sourceMetroLong = float(sourceMetro['coordinates'].split(", ")[1])
        routeFromSourceToMetro = json.loads(getDistanceAndTime(sourceLat, sourceLong, sourceMetroLat, sourceMetroLong))
        timeFromSourceToMetro = routeFromSourceToMetro["time_value"]
        # if time from source to metro itself exceeds direct pathing time, remove
        if timeFromSourceToMetro > directTime:
            nearestMetroLocationsToSource.remove(sourceMetro)

    # similarly for destination
    for destMetro in nearestMetroLocationsToDest:
        destMetroLat = float(destMetro['coordinates'].split(", ")[0])
        destMetroLong = float(destMetro['coordinates'].split(", ")[1])
        routeFromMetroToDest = json.loads(getDistanceAndTime(destMetroLat, destMetroLong, destLat, destLong))
        timeFromMetroToDest = routeFromMetroToDest["time_value"]
        # if time from source to metro itself exceeds direct pathing time, remove
        if timeFromMetroToDest > directTime:
            nearestMetroLocationsToSource.remove(destMetro)

    return nearestMetroLocationsToSource, nearestMetroLocationsToDest


def getTotalJourneyTime(sourceLat, sourceLong, destLat, destLong, sourceMetro, destMetro):
    totalTime = 0
    totalPrice = 0
    sourceMetroLat = sourceMetro["coordinates"].split(", ")[0]
    sourceMetroLong = sourceMetro["coordinates"].split(", ")[1]
    destMetroLat = destMetro["coordinates"].split(", ")[0]
    destMetroLong = destMetro["coordinates"].split(", ")[1]

    # Step 1 - get time taken from source to sourceMetro
    sourceCabFound = False
    firstLeg = getUberData(sourceLat, sourceLong, sourceMetroLat, sourceMetroLong)
    firstLegPrice = 0
    if firstLeg['prices'] is not None:
        if len(firstLeg['prices']) > 0:
            sourceCabFound = True
            firstLegTime = firstLeg['prices'][0]['duration']
            firstLegPrice = firstLeg['prices'][0]['estimate']
            firstLegPrice = firstLegPrice[1:].split('-')[0]
            totalTime = totalTime + int(firstLegTime)
            totalPrice = totalPrice + int(firstLegPrice)

    # Step 2 - get next ETA for bus/metro from that station
    waitingTime = 500
    totalTime = totalTime + int(waitingTime)

    # Step 3 - time taken to travel from sourceMetro to destMetro
    secondLeg = []
    secondLegTime = 1800
    secondLegPrice = 25
    totalTime = totalTime + int(secondLegTime)
    totalPrice = totalPrice + int(secondLegPrice)

    # Step 4 - time taken to travel from destMetro to dest
    destCabFound = False
    endLegPrice = 0
    endLeg = getUberData(destMetroLat, destMetroLong, destLat, destLong)
    if endLeg['prices'] is not None:
        if len(endLeg['prices']) > 0:
            destCabFound = True
            endLegTime = endLeg['prices'][0]['duration']
            endLegPrice = endLeg['prices'][0]['estimate']
            endLegPrice = endLegPrice[1:].split('-')[0]
            totalTime = totalTime + int(endLegTime)
            totalPrice = totalPrice + int(endLegPrice)

    # Step 5 - add all times, including the waiting time
    result = {
        "totalTime": totalTime,
        "totalPrice": totalPrice,
        "isSourceCab": sourceCabFound,
        "isDestCab": destCabFound,
        "firstLegPrice": firstLegPrice,
        "endLegPrice": endLegPrice
    }
    return result

def getUberData(sourceLat, sourceLong, destLat, destLong):
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
    routeData = requests.request("GET", uberApiURL, headers=uberHeaders, params=uberQueryString)
    routeData = routeData.json()
    return routeData


print(getFastestRoute(28.6, 77.2, 28.5, 77.32))
# getPublicTransport(28.6, 77.2, 28.5, 77.32)
# getUberData(28.6, 77.2, 28.5, 77.32)

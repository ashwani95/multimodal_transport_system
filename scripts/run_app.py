import json
from get_travel_duration import create_tranform_set,predict_time
from api.distance_matrix_api import getDistanceAndTime

def start_app():
    create_tranform_set()
    print("\nWelcome to Centralised Commutting System\n")
    print("\n-------------------------------------------\n")
    print("\nEnter the below details for find your travel iternary\n")
    print("\nInput Starting Location : (Latitude,Longitude)\n")
    sourceLat = float(input("Latitude : "))
    sourceLong = float(input("Longitude : "))
    print("\nInput Destination Location : (Latitude,Longitude)\n")
    destLat = float(input("Latitude : "))
    destLong = float(input("Longitude : "))


    distance_matrix_result = json.loads(getDistanceAndTime(sourceLat,sourceLong,destLat,destLong))
    print("\nJourney Dsitance : "+str(distance_matrix_result["distance_text"]))
    journey_time = predict_time(float(distance_matrix_result["distance_value"]),float(distance_matrix_result["time_value"]))
    print("\nEstimated Time Duration :"+journey_time)



start_app()

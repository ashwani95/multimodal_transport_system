import json
from get_travel_duration import create_tranform_set,predict_time
from api.distance_matrix_api import getDistanceAndTime

def start_app():
    create_tranform_set()
    print("\n-------------------------------------------\n")
    print("\nWelcome to Centralised Commutting System\n")

    booking = True
    while(booking):
        status = create_travel_iternary()
        if not status:
            booking = False

def create_travel_iternary():
    print("\n-------------------------------------------\n")
    print("\nEnter the below details for find your travel iternary\n")
    print("\nInput Starting Location : (Latitude,Longitude)\n")
    sourceLat = float(input("Latitude : "))
    sourceLong = float(input("Longitude : "))
    print("\nInput Destination Location : (Latitude,Longitude)\n")
    destLat = float(input("Latitude : "))
    destLong = float(input("Longitude : "))



    distance_matrix_result = json.loads(getDistanceAndTime(sourceLat, sourceLong, destLat, destLong))
    print("\n-------------------------------------------\n")
    print("\nJourney Dsitance : " + str(distance_matrix_result["distance_text"]))
    journey_time = predict_time(float(distance_matrix_result["distance_value"]),
                                float(distance_matrix_result["time_value"]))
    print("\nEstimated Time Duration :" + journey_time)

    print("\n-------------------------------------------\n")

    print("\nPress 1 to continue for another trip. Press 2 to exit\n")
    choice = int(input("Your Option : "))
    if choice == 1:
        return True
    else:
        print("\nEnjoy Your Trip :D Bye!!\n")
        return False


start_app()

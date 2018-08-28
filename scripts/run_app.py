import json
from get_travel_duration import create_tranform_set,predict_time
from api.distance_matrix_api import getDistanceAndTime
from api.get_public_transport import getFastestRoute,getCabData
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

    print("\nSelect option if you belong to the following categories :\n")
    print("\nPress 1 if you are Differently Abled \n")
    print("\nPress 2 if you are Pregnant \n")
    print("\nPress3 if you are Senior Citizen\n")
    print("\nPress 4 if you are a Minor\n")
    print("\nPress 5 if you don't belong to any of the above categories\n")
    person_type = int(input("Your option : "))

    print("\nGive us a moment, we are creating your travel iternary ...\n")
    if person_type == 5 :
        travel_iternary = json.loads(getFastestRoute(sourceLat, sourceLong, destLat, destLong))
        print("\n-------------------------------------------\n")
        print("\n"+str(travel_iternary["message"]))
        print("\nJourney Cost : Rs "+str(travel_iternary["totalPrice"]))

    else:
        travel_iternary = json.loads(getCabData(sourceLat, sourceLong, destLat, destLong))
        print("\n-------------------------------------------\n")
        print("\n"+str(travel_iternary["message"]))
        print("\nJourney Cost : Rs "+str(travel_iternary["totalPrice"]))

    distance_matrix_result = json.loads(getDistanceAndTime(sourceLat, sourceLong, destLat, destLong))

    print("\nJourney Dsitance : " + str(distance_matrix_result["distance_text"]))
    journey_time = predict_time(float(distance_matrix_result["distance_value"]),
                                float(distance_matrix_result["time_value"]))
    print("\nEstimated Time of Journey :" + journey_time)

    print("\n-------------------------------------------\n")

    print("\nPress 1 to continue for another trip. Press 2 to exit\n")
    choice = int(input("Your Option : "))
    if choice == 1:
        return True
    else:
        print("\nEnjoy Your Trip :D Bye!!\n")
        return False


start_app()

import pickle
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn


loaded_model = pickle.load(open("resources/regression_model.sav", 'rb'))
sc_X = StandardScaler()
sc_y = StandardScaler()
def create_tranform_set():
    with open("resources/distance_time_uber_movement.json") as datafile:
        data = json.load(datafile)
    dataset = pd.DataFrame(data)

    X = dataset.iloc[:, 0:1].values
    y = dataset.iloc[:, 1:2].values



    X = sc_X.fit_transform(X)
    y = sc_y.fit_transform(y)

def predict_time(distance,distance_matrix_time):
    distance = distance / 1000
    estimate_time = sc_y.inverse_transform(loaded_model.predict(sc_X.transform(np.array([[distance]]))))
    accuracy = (abs(distance_matrix_time - estimate_time) / estimate_time) * 100.0
    if accuracy >80 and accuracy <= 100:
        time_in_seconds =  estimate_time
    else:
        time_in_seconds =  distance_matrix_time
    minutes, seconds = divmod(time_in_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if seconds > 0:
        minutes+=1
    final_estimate_time = str(int(hours)) + " hours "+str(int(minutes))+" mins"
    return final_estimate_time

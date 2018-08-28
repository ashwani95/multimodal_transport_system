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

def predict_time(distance):
    y_pred = sc_y.inverse_transform(loaded_model.predict(sc_X.transform(np.array([[distance]]))))
    print(y_pred)

create_tranform_set()
i = 0
while i<=100:
    predict_time(i)
    i+=1

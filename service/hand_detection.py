import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from model.hand_features_model import HandGestureFeaturesModel


def predict_handgesture_language(input):
    model = pickle.load(open("./assets/ml_model/datasetsibi.pkl", "rb"))

    prediction = model.predict(input)

    # data = np.array(prediction)
    # data = data.tolist()

    # return prediction
    return prediction

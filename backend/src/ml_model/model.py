# src/ml/model.py

import joblib
import numpy as np
import os

# Path to the pretrained model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

# List of features in order expected by the model
feature_order = ['function_count', 'variable_count', 'binop_count', 'avg_param_count', 'function_call_count']

# Load the model once when this module is imported
model = joblib.load(MODEL_PATH)

def predict_score(features_dict):
    """
    Given a dictionary of features, predict a score between 0 and 100 using the pretrained model.
    """
    # Create a feature vector in the expected order, using 0 for missing features
    feature_vector = np.array([features_dict.get(f, 0) for f in feature_order]).reshape(1, -1)

    # Predict the score using the loaded model
    score = model.predict(feature_vector)[0]

    # Clamp and round the score to ensure it is between 0 and 100
    return min(max(round(score), 0), 100)

# src/ml_model/model.py

import joblib
import numpy as np
import os

# Path to the pretrained model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

# --- THIS IS THE FIX ---
# The list of features must EXACTLY match the keys in the dictionary 
# produced by feature_extractor.py. We've updated 'binop_count'.
feature_order = [
    'function_count', 
    'variable_count', 
    'binary_operator_count', # <-- Updated from 'binop_count'
    'avg_param_count', 
    'function_call_count'
]
# --- END OF FIX ---

# Load the model once when this module is imported
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    # Handle the case where the model file doesn't exist yet
    print(f"Warning: Model file not found at {MODEL_PATH}. The app might fail at prediction.")
    model = None

def predict_score(features_dict):
    """
    Given a dictionary of features, predict a score between 0 and 100 using the pretrained model.
    """
    if model is None:
        raise RuntimeError("ML model is not loaded. Cannot make predictions.")

    # Create a feature vector in the expected order, using 0 for missing features
    feature_vector = np.array([features_dict.get(f, 0) for f in feature_order]).reshape(1, -1)

    # Predict the score using the loaded model
    score = model.predict(feature_vector)[0]

    # Clamp and round the score to ensure it is between 0 and 100
    return min(max(round(score), 0), 100)
# src/ml/train_model.py

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/training_data.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

# Load CSV training data
df = pd.read_csv(DATA_PATH)

# Features and labels
X = df.drop(columns=['score']).values
y = df['score'].values

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model
joblib.dump(model, MODEL_PATH)
print("✅ Model trained and saved at", MODEL_PATH)

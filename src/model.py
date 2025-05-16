import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from .feature_extractor import extract_features
import numpy as np

class CodeScoringModel:
    def __init__(self):
        self.model = LinearRegression()

    def train_from_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        X = []
        y = []

        for code, score in zip(df['code'], df['score']):
            try:
                features = extract_features(code)
                X.append(features)
                y.append(score)
            except Exception as e:
                print(f"Skipping code due to error: {e}")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        print("MAE:", mean_absolute_error(y_test, y_pred))
        print("R2 Score:", r2_score(y_test, y_pred))

    def predict_score(self, code: str) -> float:
        features = np.array(extract_features(code)).reshape(1, -1)
        return round(self.model.predict(features)[0], 2)
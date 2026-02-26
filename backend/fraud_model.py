"""
fraud_model.py — 4 feature version
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "fraud_model.pkl"


# ======================
# TRAIN MODEL
# ======================
def train_model(data_path="C:/Users/Rohan/Downloads/credit_risk_data.xls"):
    print("Loading dataset...")
    df = pd.read_csv(data_path)

    REQUIRED_COLS = [
        "amount",
        "time_gap",
        "device_score",
        "location_risk",
        "is_fraud",
    ]

    for col in REQUIRED_COLS:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    X = df[["amount", "time_gap", "device_score", "location_risk"]]
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training model...")
    model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
    )

    model.fit(X_train, y_train)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("✅ Model saved!")


# ======================
# LOAD MODEL
# ======================
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Train first.")

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


# ======================
# PREDICT
# ======================
def predict_risk(features_list):
    model = load_model()

    features = np.array(features_list).reshape(1, -1)

    probability = model.predict_proba(features)[0][1]
    prediction = model.predict(features)[0]

    if probability > 0.8:
        action = "BLOCK"
    elif probability > 0.5:
        action = "STEP_UP_AUTH"
    else:
        action = "ALLOW"

    return {
        "fraud_probability": float(probability),
        "prediction": int(prediction),
        "action": action,
    }


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    train_model()
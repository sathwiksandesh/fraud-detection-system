import pickle
import numpy as np

# Load model
with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

def calculate_risk(transaction_features):
    features = np.array(transaction_features).reshape(1, -1)
    probability = model.predict_proba(features)[0][1]

    if probability > 0.8:
        action = "BLOCK"
    elif probability > 0.5:
        action = "STEP_UP_AUTH"
    else:
        action = "ALLOW"

    return {
        "risk_score": float(probability),
        "action": action
    }
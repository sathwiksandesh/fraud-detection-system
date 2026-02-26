from fastapi import FastAPI
from pydantic import BaseModel
from fraud_model import predict_risk

app = FastAPI(title="Fraud Detection API")


# optional but recommended
@app.get("/")
def home():
    return {"message": "Fraud Detection API is running"}


class Transaction(BaseModel):
    amount: float
    time_gap: float
    device_score: float
    location_risk: float


@app.post("/check_transaction")
def check_transaction(txn: Transaction):

    features = [
        txn.amount,
        txn.time_gap,
        txn.device_score,
        txn.location_risk
    ]

    result = predict_risk(features)
    return result
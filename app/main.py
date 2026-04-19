from fastapi import FastAPI, HTTPException
import joblib
from pathlib import Path

from app.schemas import PredictionRequest, PredictionResponse

app = FastAPI()

MODEL_PATH = Path("models/model.joblib")

model = None
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)


@app.get("/")
def read_root():
    return {"message": "Taxi demand prediction API is running"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    features = [[
        request.hour,
        request.day_of_week,
        request.month,
        request.is_weekend,
        request.lag_1,
        request.lag_24,
        request.rolling_24,
    ]]

    prediction = model.predict(features)[0]
    return PredictionResponse(prediction=float(prediction))
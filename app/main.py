from fastapi import FastAPI
import joblib

from app.schemas import PredictionRequest, PredictionResponse

# init
app = FastAPI()

# load in the model
model = joblib.load("models/model.joblib")

@app.get("/")
def read_root():
    return {"message": "Taxi demand prediction API is running"}

# response must match prediction response
@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
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
from pydantic import BaseModel
# schema check

class PredictionRequest(BaseModel):
    hour: int
    day_of_week: int
    month: int
    is_weekend: int
    lag_1: float
    lag_24: float
    rolling_24: float


class PredictionResponse(BaseModel):
    prediction: float
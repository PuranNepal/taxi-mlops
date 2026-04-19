from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_predict():
    payload = {
        "hour": 14,
        "day_of_week": 2,
        "month": 1,
        "is_weekend": 0,
        "lag_1": 5,
        "lag_24": 8,
        "rolling_24": 6.2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
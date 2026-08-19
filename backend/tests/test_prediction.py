from fastapi.testclient import TestClient
from app.main import app

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

def test_predict_happy_path():
    payload = {
        "location": "thane",
        "area_sqft": 1000.0,
        "floor_num": 5,
        "bathroom": 2,
        "balcony": 1,
        "parking": 1,
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East",
        "status": "Ready to Move"
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        assert "predicted_price" in response.json()
        assert isinstance(response.json()["predicted_price"], float)

def test_predict_invalid_input():
    payload = {
        "location": "thane"
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

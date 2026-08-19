from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.inference import predict

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/predict", response_model=PredictionResponse)
def make_prediction(request: PredictionRequest):
    price = predict(request.model_dump())
    return PredictionResponse(predicted_price=price)

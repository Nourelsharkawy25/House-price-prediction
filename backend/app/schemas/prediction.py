from pydantic import BaseModel

class PredictionRequest(BaseModel):
    location: str
    area_sqft: float
    floor_num: int
    bathroom: int
    balcony: int
    parking: int
    furnishing: str
    transaction: str
    ownership: str
    facing: str
    status: str

class PredictionResponse(BaseModel):
    predicted_price: float

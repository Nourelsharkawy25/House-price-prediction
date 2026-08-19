import joblib
from app.core.config import settings
from app.services.preprocessing import preprocess_request

model = None

def load_model():
    global model
    model = joblib.load(settings.MODEL_PATH)
    
def predict(data: dict) -> float:
    df = preprocess_request(data)
    pred = model.predict(df)[0]
    return float(pred)

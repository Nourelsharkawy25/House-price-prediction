import pandas as pd
import json
from app.core.config import settings

def _load_locations():
    try:
        with open(settings.LOCATIONS_PATH, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

VALID_LOCATIONS = _load_locations()

def preprocess_request(data: dict) -> pd.DataFrame:
    loc = data["location"]
    if loc not in VALID_LOCATIONS:
        loc = "other"
        
    row = {
        "area_sqft": data["area_sqft"],
        "floor_num": data["floor_num"],
        "bathroom_num": data["bathroom"],
        "balcony_num": data["balcony"],
        "parking_num": data["parking"],
        "location_clean": loc,
        "Furnishing": data["furnishing"],
        "Transaction": data["transaction"],
        "Ownership": data["ownership"],
        "facing": data["facing"],
        "Status": data["status"]
    }
    
    return pd.DataFrame([row])

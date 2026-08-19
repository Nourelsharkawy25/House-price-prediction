from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODEL_PATH: str = "models/house_price.pkl"
    LOCATIONS_PATH: str = "models/locations.json"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

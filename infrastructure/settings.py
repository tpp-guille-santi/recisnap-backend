import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_NAME: str = 'recisnap'
    LOG_LEVEL: int = logging.INFO
    MONGO_URL: str
    FIREBASE_CREDENTIALS_PATH: str
    FIREBASE_STORAGE_BASE_URL: str
    GEOREF_STORAGE_BASE_URL: str


settings = Settings()

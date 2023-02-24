import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_NAME: str = 'recisnap'
    LOG_LEVEL: int = logging.INFO
    MONGO_URL: str
    FIREBASE_CREDENTIALS: str
    FIREBASE_STORAGE_BASE_URL: str
    GEOREF_BASE_URL: str


settings = Settings()

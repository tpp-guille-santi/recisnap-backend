import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_NAME: str = 'recisnap'
    LOG_LEVEL: int = logging.INFO
    MONGO_URL: str
    FIREBASE_CREDENTIALS: str
    FIREBASE_STORAGE_BASE_URL: str
    GEOREF_BASE_URL: str
    DETA_DRIVE: str
    DETA_DRIVE_KEY: str


settings = Settings()

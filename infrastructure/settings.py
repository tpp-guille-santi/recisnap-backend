import logging
import os

LOG_LEVEL = int(os.getenv('LOG_LEVEL', logging.INFO))
MONGO_URL = os.environ['MONGO_URL']

DATABASE_NAME = 'recisnap'
FIREBASE_STORAGE_BASE_URL = os.environ['FIREBASE_STORAGE_BASE_URL']
GEOREF_STORAGE_BASE_URL = os.environ['GEOREF_STORAGE_BASE_URL']
DEFAULT_MODEL = 'model.h5'
IMAGE_SIZE = (224, 224)

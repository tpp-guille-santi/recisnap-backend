import logging
import os

LOG_LEVEL = int(os.getenv('LOG_LEVEL', logging.INFO))
MODEL_NAMES_LOCATION = os.getenv('MODEL_NAMES_LOCATION', './materials.txt')
MODEL_LOCATION = os.getenv('MODEL_LOCATION', 'tensor_simplificado.pt')
MONGO_URL = os.environ["MONGODB_URL"]

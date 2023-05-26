import json
import logging
import uuid

import firebase_admin
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials

from app.infrastructure.context import trace_id
from app.infrastructure.logs import configure_logging
from app.infrastructure.routers import health
from app.infrastructure.routers import images
from app.infrastructure.routers import instructions
from app.infrastructure.routers import materials
from app.infrastructure.routers import users
from app.infrastructure.settings import settings

LOGGER = logging.getLogger(__name__)

cred = credentials.Certificate({**json.loads(settings.FIREBASE_CREDENTIALS)})
firebase_admin.initialize_app(cred)

app = FastAPI(
    title='Image Predictor Service',
    version='1.0',
    description='API to predict the material from an image.',
)


@app.on_event('startup')
async def startup_event():
    configure_logging(settings.LOG_LEVEL)


@app.middleware('http')
async def requests_middleware(request: Request, call_next):
    trace_id.set(str(uuid.uuid4()))
    response = await call_next(request)
    return response


origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(materials.router)
app.include_router(instructions.router)
app.include_router(images.router)

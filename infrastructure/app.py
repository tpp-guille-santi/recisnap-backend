import logging
import uuid

from fastapi import FastAPI, HTTPException, Request

from infrastructure import views
from infrastructure.context import trace_id
from infrastructure.exceptions_handlers import http_exception_handler
from infrastructure.logs import configure_logging
from infrastructure.settings import LOG_LEVEL

LOGGER = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title='Image Predictor Service',
        version='1.0',
        description='API to predict the material from an image.'
    )

    @app.on_event("startup")
    async def startup_event():
        configure_logging(LOG_LEVEL)

    @app.middleware("http")
    async def requests_middleware(request: Request, call_next):
        trace_id.set(str(uuid.uuid4()))
        response = await call_next(request)
        if request.url.path != '/health':
            LOGGER.info(f'{request.method} - {request.url.path} :  {response.status_code}')
        return response

    app.include_router(views.router)
    app.add_exception_handler(HTTPException, http_exception_handler)
    return app

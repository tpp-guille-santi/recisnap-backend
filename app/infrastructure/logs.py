import logging

from app.infrastructure.context import trace_id

LOGGER_FORMAT = '[%(asctime)s] [%(levelname)s] [%(trace_id)s] [%(name)s] %(message)s'


def _create_logger_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(TaskFormatter(LOGGER_FORMAT))
    return handler


def configure_logging(level):
    handler = logging.StreamHandler()
    handler.setFormatter(TaskFormatter(LOGGER_FORMAT))
    logging.basicConfig(level=level, force=True, handlers=[handler])
    uvicorn_logger = logging.getLogger('uvicorn.access')
    if not uvicorn_logger.handlers:
        uvicorn_logger.addHandler(handler)
    else:
        uvicorn_logger.handlers[0].setFormatter(TaskFormatter(LOGGER_FORMAT))


class TaskFormatter(logging.Formatter):
    def format(self, record):
        record.__dict__.setdefault('trace_id', trace_id.get())
        return super().format(record)

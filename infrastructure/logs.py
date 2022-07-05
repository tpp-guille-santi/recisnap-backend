import logging

from infrastructure.context import trace_id

LOGGER_FORMAT = '[%(asctime)s] [%(levelname)s] [%(trace_id)s] [%(name)s] %(message)s'


def _create_logger_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(TaskFormatter(LOGGER_FORMAT))
    return handler


def configure_logging(level):
    logging.basicConfig(level=level, handlers=[_create_logger_handler()])


class TaskFormatter(logging.Formatter):

    def __init__(self, fmt):
        super().__init__(fmt=fmt)

    def format(self, record):
        record.__dict__.setdefault('trace_id', trace_id.get())
        return super().format(record)

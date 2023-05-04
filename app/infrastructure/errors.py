from fastapi import HTTPException
from fastapi import status


class FileTypeExceptionException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        self.detail = 'The image format is not supported'


class ModelReplacementException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = 'Could not replace the model'

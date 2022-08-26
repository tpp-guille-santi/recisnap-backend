from fastapi import HTTPException, status


class FileTypeExceptionException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        self.detail = 'The image format is not supported'


class ModelReplacementException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = 'Could not replace the model'


class UserNotFoundException(HTTPException):
    def __init__(self, id: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'User {id} not found'

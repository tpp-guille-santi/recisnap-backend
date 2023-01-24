from fastapi import HTTPException
from fastapi import status
from odmantic import ObjectId


class UserNotFoundException(HTTPException):
    def __init__(self, id: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'User {id} not found'


class PageNotFoundException(HTTPException):
    def __init__(self, id: ObjectId):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'Page {id} not found'


class MaterialNotFoundException(HTTPException):
    def __init__(self, id: ObjectId):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'Material {id} not found'


class ModelNotFoundException(HTTPException):
    def __init__(self, id: ObjectId):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'Model {id} not found'


class NoModelsFoundException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = 'There are no models available'

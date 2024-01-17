from fastapi import HTTPException
from fastapi import status
from odmantic import ObjectId


class PageNotFoundException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = 'Page not found'


class UserNotFoundException(HTTPException):
    def __init__(self, id: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'User {id} not found'


class InstructionNotFoundException(HTTPException):
    def __init__(self, id: ObjectId):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'Instruction {id} not found'


class MaterialNotFoundException(HTTPException):
    def __init__(self, id: ObjectId):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'Material {id} not found'


class ModelNotFoundException(HTTPException):
    def __init__(self, id: ObjectId):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'Model {id} not found'


class ImageNotFoundException(HTTPException):
    def __init__(self, id: ObjectId):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f'Image {id} not found'


class NoModelsFoundException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = 'There are no models available'

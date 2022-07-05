from fastapi import HTTPException, status


class FileTypeExceptionException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        self.detail = 'The file should be an image'

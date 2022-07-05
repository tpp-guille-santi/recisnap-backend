from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request,
                                 exception: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exception.status_code, content={'message': exception.detail})

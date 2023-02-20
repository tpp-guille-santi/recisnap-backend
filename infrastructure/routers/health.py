import logging

from fastapi import APIRouter
from fastapi import Response
from fastapi import status

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix='/health',
    tags=['health'],
)


@router.get('/')
async def health() -> Response:
    return Response(status_code=status.HTTP_200_OK, content='OK')

import io
import logging

import requests
from PIL import Image
from fastapi import APIRouter, Response, UploadFile, Depends

from domain.usecases import UseCases
from infrastructure.errors import FileTypeExceptionException
from infrastructure.settings import MODEL_LOCATION, MODEL_NAMES_LOCATION

LOGGER = logging.getLogger(__name__)

router = APIRouter(tags=['test'])

usecases = UseCases(MODEL_LOCATION, MODEL_NAMES_LOCATION)


@router.get('/health')
async def health() -> Response:
    return Response(status_code=requests.codes.ok, content='OK')


async def get_image(file: UploadFile):
    # image_extensions = ['ras', 'xwd', 'bmp', 'jpe', 'jpg', 'jpeg', 'xpm', 'ief', 'pbm', 'tif',
    #                     'gif', 'ppm', 'xbm', 'tiff', 'rgb', 'pgm', 'png', 'pnm']
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        image = Image.open(io.BytesIO(image_bytes))
        return image
    except Exception:
        raise FileTypeExceptionException()


@router.post('/images')
async def predict_material(image: Image = Depends(get_image)):
    material = await usecases.predict_material(image)

    return material

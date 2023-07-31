import logging
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Query
from fastapi import Response
from fastapi import status
from fastapi.responses import StreamingResponse
from odmantic import ObjectId

from app.domain.entities import Image
from app.domain.entities import ImageSearch
from app.domain.entities import ImageUpdate
from app.domain.usecases.images_usecases import ImagesUseCases
from app.infrastructure.dependencies import images_usecases_dependency
from app.infrastructure.schemas import ImagesCountResponse

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix='/images',
    tags=['images'],
)


@router.post('/', response_model=Image, status_code=status.HTTP_201_CREATED)
async def create_image(
    image: Image,
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    image = await images_usecases.create_image(image)
    return image


@router.get('/', response_model=list[Image])
async def list_images(
    filename: Union[str, None] = None,
    material_name: Union[str, None] = None,
    tags: Union[list[str], None] = Query(default=None),
    downloaded: Union[bool, None] = None,
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    params = ImageSearch(
        filename=filename, material_name=material_name, tags=tags, downloaded=downloaded
    )
    images = await images_usecases.list_images(params)
    return images


@router.get('/count/', response_model=ImagesCountResponse)
async def get_images_count(
    filename: Union[str, None] = None,
    material_name: Union[str, None] = None,
    tags: Union[list[str], None] = Query(default=None),
    downloaded: Union[bool, None] = None,
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    params = ImageSearch(
        filename=filename, material_name=material_name, tags=tags, downloaded=downloaded
    )
    count = await images_usecases.get_images_count(params)
    return ImagesCountResponse(count=count)


@router.get('/{id}/', response_model=Image)
async def get_image_by_id(
    id: ObjectId,
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    image = await images_usecases.get_image_by_id(id)
    return image


@router.patch('/{id}/', response_model=Image)
async def update_image_by_id(
    id: ObjectId,
    patch: ImageUpdate,
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    image = await images_usecases.update_image_by_id(id, patch)
    return image


@router.delete('/{id}/', response_model=Image)
async def delete_image_by_id(
    id: ObjectId,
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    image = await images_usecases.delete_image_by_id(id)
    return image


@router.post('/file/{filename}/')
async def upload_image(
    filename: str,
    file: bytes = File(),
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    await images_usecases.upload_image(filename, file)
    return Response()


@router.get('/file/{filename}/')
async def download_image(
    filename: str,
    images_usecases: ImagesUseCases = Depends(images_usecases_dependency),
):
    file = await images_usecases.download_image(filename)
    return StreamingResponse(content=file, media_type='text/plain')

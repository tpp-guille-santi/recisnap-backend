import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from odmantic import ObjectId

from app.domain.entities import MLModel
from app.domain.entities import MLModelUpdate
from app.domain.entities import Pagination
from app.domain.usecases.models_usecases import ModelsUseCases
from app.infrastructure.dependencies import models_usecases_dependency

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix='/models',
    tags=['models'],
)


@router.post('/', response_model=MLModel, status_code=status.HTTP_201_CREATED)
async def create_model(
    model: MLModel,
    models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
):
    model = await models_usecases.create_model(model)
    return model


@router.get('/latest/', response_model=MLModel)
async def get_latest_model(
    models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
):
    model = await models_usecases.get_latest_model()
    return model


@router.get('/', response_model=Pagination)
async def list_models(
    page: int = 0,
    page_size: int = 10,
    models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
):
    models = await models_usecases.list_models(page=page, page_size=page_size)
    return models


@router.get('/{id}/', response_model=MLModel)
async def get_model_by_id(
    id: ObjectId, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
):
    model = await models_usecases.get_model_by_id(id)
    return model


@router.patch('/{id}/', response_model=MLModel)
async def update_model_by_id(
    id: ObjectId,
    patch: MLModelUpdate,
    models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
):
    model = await models_usecases.update_model_by_id(id, patch)
    return model


@router.delete('/{id}/', response_model=MLModel)
async def delete_model_by_id(
    id: ObjectId, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
):
    model = await models_usecases.delete_model_by_id(id)
    return model

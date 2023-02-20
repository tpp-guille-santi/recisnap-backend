import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from odmantic import ObjectId

from domain.entities import Material
from domain.entities import MaterialUpdate
from domain.usecases.materials_usecases import MaterialsUseCases
from infrastructure.dependencies import materials_usecases_dependency

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix='/materials',
    tags=['materials'],
)


@router.post('/', response_model=Material, status_code=status.HTTP_201_CREATED)
async def create_material(
    material: Material,
    materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
):
    material = await materials_usecases.create_material(material)
    return material


@router.get('/', response_model=list[Material])
async def list_materials(
    enabled: bool | None = None,
    materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
):
    materials = await materials_usecases.list_materials(enabled)
    return materials


@router.get('/{id}', response_model=Material)
async def get_material_by_id(
    id: ObjectId, materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency)
):
    material = await materials_usecases.get_material_by_id(id)
    return material


@router.patch('/{id}', response_model=Material)
async def update_material_by_id(
    id: ObjectId,
    patch: MaterialUpdate,
    materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
):
    material = await materials_usecases.update_material_by_id(id, patch)
    return material


@router.delete('/{id}', response_model=Material)
async def delete_material_by_id(
    id: ObjectId, materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency)
):
    material = await materials_usecases.delete_material_by_id(id)
    return material

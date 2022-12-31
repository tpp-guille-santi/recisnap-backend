import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from odmantic import ObjectId

from domain.entities import Material
from domain.entities import MaterialUpdate
from domain.entities import Page
from domain.entities import PageResponse
from domain.entities import PageSearch
from domain.entities import PageUpdate
from domain.entities import User
from domain.entities import UserUpdate
from domain.usecases.materials_usecases import MaterialsUseCases
from domain.usecases.pages_usecases import PagesUseCases
from domain.usecases.users_usecases import UsersUseCases
from infrastructure.dependencies import materials_usecases_dependency
from infrastructure.dependencies import pages_usecases_dependency
from infrastructure.dependencies import users_usecases_dependency
from infrastructure.settings import FIREBASE_STORAGE_BASE_URL

LOGGER = logging.getLogger(__name__)

router = APIRouter(tags=['test'])


@router.get('/health')
async def health() -> Response:
    return Response(status_code=status.HTTP_200_OK, content='OK')


# async def _get_image(file: UploadFile):
#     try:
#         image_bytes = await file.read()
#         image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
#         image.verify()
#         return Image.open(io.BytesIO(image_bytes)).convert('RGB')
#     except Exception:
#         raise FileTypeExceptionException()


# @router.post('/images')
# async def predict_material(
#         model_name: str = DEFAULT_MODEL,
#         image: Image = Depends(_get_image),
#         usecases: UseCases = Depends(usecases_dependency),
#         materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
#         models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     material = await usecases.predict_material(image, model_name, materials_usecases,
#                                                models_usecases)
#     return material


@router.post('/users', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User, users_usecases: UsersUseCases = Depends(users_usecases_dependency)
):
    user = await users_usecases.create_user(user)
    return user


@router.get('/users', response_model=list[User])
async def list_users(users_usecases: UsersUseCases = Depends(users_usecases_dependency)):
    users = await users_usecases.list_users()
    return users


@router.get('/users/{id}', response_model=User)
async def get_user_by_id(
    id: ObjectId, users_usecases: UsersUseCases = Depends(users_usecases_dependency)
):
    user = await users_usecases.get_user_by_id(id)
    return user


@router.patch('/users/{id}', response_model=User)
async def update_user_by_id(
    id: ObjectId,
    patch: UserUpdate,
    users_usecases: UsersUseCases = Depends(users_usecases_dependency),
):
    user = await users_usecases.update_user_by_id(id, patch)
    return user


@router.delete('/users/{id}', response_model=User)
async def delete_user_by_id(
    id: ObjectId, users_usecases: UsersUseCases = Depends(users_usecases_dependency)
):
    user = await users_usecases.delete_user_by_id(id)
    return user


@router.post('/materials', response_model=Material, status_code=status.HTTP_201_CREATED)
async def create_material(
    material: Material,
    materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
):
    material = await materials_usecases.create_material(material)
    return material


@router.get('/materials', response_model=list[Material])
async def list_materials(
    enabled: bool | None = None,
    materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
):
    materials = await materials_usecases.list_materials(enabled)
    return materials


@router.get('/materials/{id}', response_model=Material)
async def get_material_by_id(
    id: ObjectId, materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency)
):
    material = await materials_usecases.get_material_by_id(id)
    return material


@router.patch('/materials/{id}', response_model=Material)
async def update_material_by_id(
    id: ObjectId,
    patch: MaterialUpdate,
    materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
):
    material = await materials_usecases.update_material_by_id(id, patch)
    return material


@router.delete('/materials/{id}', response_model=Material)
async def delete_material_by_id(
    id: ObjectId, materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency)
):
    material = await materials_usecases.delete_material_by_id(id)
    return material


# @router.post('/models', response_model=MLModel, status_code=status.HTTP_201_CREATED)
# async def create_model(
#         model: MLModel, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     model = await models_usecases.create_model(model)
#     return model
#
#
# @router.get('/models', response_model=list[MLModel])
# async def list_models(
#         limit: int | None = None,
#         name: str | None = None,
#         models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
# ):
#     models = await models_usecases.list_models(limit, name)
#     return models
#
#
# @router.get('/models/{id}', response_model=MLModel)
# async def get_model_by_id(
#         id: ObjectId, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     model = await models_usecases.get_model_by_id(id)
#     return model
#
#
# @router.patch('/models/{id}', response_model=MLModel)
# async def update_model_by_id(
#         id: ObjectId,
#         patch: MLModelUpdate,
#         models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
# ):
#     model = await models_usecases.update_model_by_id(id, patch)
#     return model
#
#
# @router.delete('/models/{id}', response_model=MLModel)
# async def delete_model_by_id(
#         id: ObjectId, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     model = await models_usecases.delete_model_by_id(id)
#     return model


@router.post('/pages', response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    page: Page, pages_usecases: PagesUseCases = Depends(pages_usecases_dependency)
):
    page = await pages_usecases.create_page(page)
    return PageResponse.from_entity(page, FIREBASE_STORAGE_BASE_URL)


@router.get('/pages', response_model=list[PageResponse])
async def list_pages(pages_usecases: PagesUseCases = Depends(pages_usecases_dependency)):
    pages = await pages_usecases.list_pages()
    return [PageResponse.from_entity(page, FIREBASE_STORAGE_BASE_URL) for page in pages]


@router.post('/pages/search', response_model=list[PageResponse])
async def search_pages(
    search: PageSearch,
    pages_usecases: PagesUseCases = Depends(pages_usecases_dependency),
):
    pages = await pages_usecases.search_pages(search)
    return [PageResponse.from_entity(page, FIREBASE_STORAGE_BASE_URL) for page in pages]


@router.get('/pages/{id}', response_model=PageResponse)
async def get_page_by_id(
    id: ObjectId, pages_usecases: PagesUseCases = Depends(pages_usecases_dependency)
):
    page = await pages_usecases.get_page_by_id(id)
    return PageResponse.from_entity(page, FIREBASE_STORAGE_BASE_URL)


@router.patch('/pages/{id}', response_model=PageResponse)
async def update_page_by_id(
    id: ObjectId,
    patch: PageUpdate,
    pages_usecases: PagesUseCases = Depends(pages_usecases_dependency),
):
    page = await pages_usecases.update_page_by_id(id, patch)
    return PageResponse.from_entity(page, FIREBASE_STORAGE_BASE_URL)


@router.delete('/pages/{id}', response_model=PageResponse)
async def delete_page_by_id(
    id: ObjectId, pages_usecases: PagesUseCases = Depends(pages_usecases_dependency)
):
    page = await pages_usecases.delete_page_by_id(id)
    return PageResponse.from_entity(page, FIREBASE_STORAGE_BASE_URL)

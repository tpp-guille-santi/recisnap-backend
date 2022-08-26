import io
import logging

import motor.motor_asyncio
from PIL import Image
from fastapi import APIRouter, Response, UploadFile, Depends, status
from fastapi.encoders import jsonable_encoder

from domain.entities import UserModel, UpdateUserModel
from domain.usecases import UseCases
from infrastructure.errors import FileTypeExceptionException, UserNotFoundException
from infrastructure.settings import MODEL_LOCATION, MODEL_NAMES_LOCATION, MONGO_URL

LOGGER = logging.getLogger(__name__)

router = APIRouter(tags=['test'])
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.recisnap

usecases = UseCases(MODEL_LOCATION, MODEL_NAMES_LOCATION)


@router.get('/health')
async def health() -> Response:
    return Response(status_code=status.HTTP_200_OK, content='OK')


async def get_image(file: UploadFile):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image.verify()
        return Image.open(io.BytesIO(image_bytes)).convert('RGB')
    except Exception:
        raise FileTypeExceptionException()


@router.post('/images')
async def predict_material(image: Image = Depends(get_image)):
    material = await usecases.predict_material(image)

    return material


@router.get('/materials')
async def get_materials():
    materials = await usecases.get_materials()

    return materials


@router.put('/models')
async def replace_model(file: UploadFile):
    await usecases.replace_model(file)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/users", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel):
    new_user = await db["users"].insert_one(jsonable_encoder(user))
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return created_user


@router.get("/users", response_model=list[UserModel])
async def list_users():
    LOGGER.info(MONGO_URL)
    users = await db["users"].find().to_list(1000)
    return users


@router.get("/users/{id}", response_model=UserModel)
async def show_user(id: str):
    user = await db["users"].find_one({"_id": id})
    if not user:
        raise UserNotFoundException(id)
    return user


@router.put("/users/{id}", response_model=UserModel)
async def update_user(id: str, user: UpdateUserModel):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = await db["users"].update_one({"_id": id}, {"$set": user})
        if update_result.modified_count == 1:
            LOGGER.info(f'Updated user {id}')
    user = await db["users"].find_one({"_id": id})
    if not user:
        raise UserNotFoundException(id)
    return user


@router.delete("/users/{id}")
async def delete_user(id: str):
    delete_result = await db["users"].delete_one({"_id": id})
    if delete_result.deleted_count != 1:
        raise UserNotFoundException(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

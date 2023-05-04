import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.domain.entities import User
from app.domain.entities import UserUpdate
from app.domain.usecases.users_usecases import UsersUseCases
from app.infrastructure.dependencies import users_usecases_dependency

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User, users_usecases: UsersUseCases = Depends(users_usecases_dependency)
):
    user = await users_usecases.create_user(user)
    return user


@router.get('/', response_model=list[User])
async def list_users(users_usecases: UsersUseCases = Depends(users_usecases_dependency)):
    users = await users_usecases.list_users()
    return users


@router.get('/{firebase_uid}/', response_model=User)
async def get_user_by_firebase_uid(
    firebase_uid: str, users_usecases: UsersUseCases = Depends(users_usecases_dependency)
):
    user = await users_usecases.get_user_by_firebase_uid(firebase_uid)
    return user


@router.patch('/{firebase_uid}/', response_model=User)
async def update_user_by_firebase_uid(
    firebase_uid: str,
    patch: UserUpdate,
    users_usecases: UsersUseCases = Depends(users_usecases_dependency),
):
    user = await users_usecases.update_user_by_firebase_uid(firebase_uid, patch)
    return user


@router.delete('/{firebase_uid}/', response_model=User)
async def delete_user_by_firebase_uid(
    firebase_uid: str, users_usecases: UsersUseCases = Depends(users_usecases_dependency)
):
    user = await users_usecases.delete_user_by_firebase_uid(firebase_uid)

    return user

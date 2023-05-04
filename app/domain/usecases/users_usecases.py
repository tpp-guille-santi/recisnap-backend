import logging

from odmantic import AIOEngine

from app.domain.entities import User
from app.domain.entities import UserUpdate
from app.domain.errors import UserNotFoundException
from app.infrastructure.repositories import FirebaseAuthRepository

LOGGER = logging.getLogger(__name__)


class UsersUseCases:
    def __init__(self, engine: AIOEngine, firebase_auth_repository: FirebaseAuthRepository):
        self.engine = engine
        self.firebase_auth_repository = firebase_auth_repository

    async def create_user(self, user: User) -> User:
        user = await self.engine.save(user)
        return user

    async def list_users(self) -> list[User]:
        users = await self.engine.find(User)
        return users

    async def get_user_by_firebase_uid(self, firebase_uid: str) -> User:
        user = await self.engine.find_one(User, User.firebase_uid == firebase_uid)
        if not user:
            raise UserNotFoundException(firebase_uid)
        return user

    async def update_user_by_firebase_uid(self, firebase_uid: str, patch: UserUpdate) -> User:
        user = await self.engine.find_one(User, User.firebase_uid == firebase_uid)
        if user is None:
            raise UserNotFoundException(firebase_uid)
        user.update(patch)
        await self.engine.save(user)
        return user

    async def delete_user_by_firebase_uid(self, firebase_uid: str) -> User:
        user = await self.engine.find_one(User, User.firebase_uid == firebase_uid)
        if user is None:
            raise UserNotFoundException(firebase_uid)
        await self.engine.delete(user)
        await self.firebase_auth_repository.delete_user(firebase_uid)
        return user

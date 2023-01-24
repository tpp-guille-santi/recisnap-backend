import logging

from odmantic import AIOEngine

from domain.entities import User
from domain.entities import UserUpdate
from domain.errors import UserNotFoundException

LOGGER = logging.getLogger(__name__)


class UsersUseCases:
    def __init__(self, engine: AIOEngine):
        self.engine = engine

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
        return user

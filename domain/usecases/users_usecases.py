from odmantic import ObjectId, AIOEngine

from domain.entities import User, UserUpdate
from domain.errors import UserNotFoundException


class UsersUseCases:

    def __init__(self, engine: AIOEngine):
        self.engine = engine

    async def create_user(self, user: User) -> User:
        user = await self.engine.save(user)
        return user

    async def list_users(self) -> list[User]:
        users = await self.engine.find(User)
        return users

    async def get_user_by_id(self, id: ObjectId) -> User:
        user = await self.engine.find_one(User, User.id == id)
        if not user:
            raise UserNotFoundException(id)
        return user

    async def update_user_by_id(self, id: ObjectId, patch: UserUpdate) -> User:
        user = await self.engine.find_one(User, User.id == id)
        if user is None:
            raise UserNotFoundException(id)
        user.update(patch)
        await self.engine.save(user)
        return user

    async def delete_user_by_id(self, id: ObjectId) -> User:
        user = await self.engine.find_one(User, User.id == id)
        if user is None:
            raise UserNotFoundException(id)
        await self.engine.delete(user)
        return user

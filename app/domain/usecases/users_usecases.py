import logging

from odmantic import AIOEngine

from app.domain.entities import Pagination
from app.domain.entities import User
from app.domain.entities import UserUpdate
from app.domain.errors import PageNotFoundException
from app.domain.errors import UserNotFoundException
from app.domain.utils import get_next_page
from app.domain.utils import get_total_pages
from app.infrastructure.repositories import FirebaseAuthRepository

LOGGER = logging.getLogger(__name__)


class UsersUseCases:
    def __init__(self, engine: AIOEngine, firebase_auth_repository: FirebaseAuthRepository):
        self.engine = engine
        self.firebase_auth_repository = firebase_auth_repository

    async def create_user(self, user: User) -> User:
        user = await self.engine.save(user)
        return user

    async def list_users(self, page: int, page_size: int) -> Pagination:
        count = await self.engine.count(User)
        total_pages = get_total_pages(count, page_size)
        if page >= total_pages:
            raise PageNotFoundException()
        items = await self.engine.find(
            User,
            skip=page * page_size,
            limit=page_size,
        )
        next_page = get_next_page(page, total_pages)
        return Pagination[User](
            count=count, next_page=next_page, page=page, page_size=page_size, items=items
        )

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

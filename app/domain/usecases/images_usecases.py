import logging

from odmantic import AIOEngine
from odmantic import ObjectId
from odmantic import query
from odmantic.query import QueryExpression

from app.domain.entities import Image
from app.domain.entities import ImageSearch
from app.domain.entities import ImageUpdate
from app.domain.entities import Pagination
from app.domain.errors import ImageNotFoundException
from app.domain.repositories import AbstractDetaDriveRepository
from app.domain.utils import get_next_page
from app.domain.utils import get_total_pages

LOGGER = logging.getLogger(__name__)


def _get_search_params(params: ImageSearch | None) -> list[QueryExpression]:
    query_filters = []
    if params is not None:
        if params.filename is not None:
            query_filters.append(Image.filename == params.filename)
        if params.material_name is not None:
            query_filters.append(Image.material_name == params.material_name)
        if params.downloaded is not None:
            query_filters.append(Image.downloaded == params.downloaded)
        if params.tags is not None:
            for tag in params.tags:
                query_filters.append(query.in_(Image.tags, [tag]))
    return query_filters


class ImagesUseCases:
    def __init__(
        self,
        engine: AIOEngine,
        deta_drive_repository: AbstractDetaDriveRepository,
    ):
        self.engine = engine
        self.deta_drive_repository = deta_drive_repository

    async def create_image(self, image: Image) -> Image:
        image = await self.engine.save(image)
        return image

    async def list_images(
        self, page: int, page_size: int, params: ImageSearch | None
    ) -> Pagination:
        query_filters = _get_search_params(params)
        count = await self.engine.count(Image, *query_filters)
        total_pages = get_total_pages(count, page_size)
        if page >= total_pages:
            page = 0
        items = await self.engine.find(
            Image,
            *query_filters,
            skip=page * page_size,
            limit=page_size,
        )
        next_page = get_next_page(page, total_pages)
        return Pagination[Image](
            count=count, next_page=next_page, page=page, page_size=page_size, items=items
        )

    async def get_image_by_id(self, id: ObjectId) -> Image:
        image = await self.engine.find_one(Image, Image.id == id)
        if not image:
            raise ImageNotFoundException(id)
        return image

    async def update_image_by_id(self, id: ObjectId, patch: ImageUpdate) -> Image:
        image = await self.engine.find_one(Image, Image.id == id)
        if image is None:
            raise ImageNotFoundException(id)
        image.update(patch)
        await self.engine.save(image)
        return image

    async def delete_image_by_id(self, id: ObjectId) -> Image:
        image = await self.engine.find_one(Image, Image.id == id)
        if image is None:
            raise ImageNotFoundException(id)
        await self.engine.delete(image)
        return image

    async def upload_image(self, filename: str, file: bytes) -> None:
        await self.deta_drive_repository.upload_file(filename, file)

    async def download_image(self, filename):
        file = await self.deta_drive_repository.download_file(filename)
        return file.iter_chunks()

    async def get_images_count(self, params: ImageSearch | None) -> int:
        query_filters = _get_search_params(params)
        count = await self.engine.count(Image, *query_filters)
        return count

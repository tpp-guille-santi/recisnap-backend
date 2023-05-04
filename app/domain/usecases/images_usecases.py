import logging

from odmantic import AIOEngine
from odmantic import ObjectId

from app.domain.entities import Image
from app.domain.entities import ImageUpdate
from app.domain.errors import ImageNotFoundException
from app.domain.repositories import AbstractDetaDriveRepository

LOGGER = logging.getLogger(__name__)


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

    async def list_images(self) -> list[Image]:
        image = await self.engine.find(Image)
        return image

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

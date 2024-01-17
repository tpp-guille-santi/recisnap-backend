import logging

from odmantic import AIOEngine
from odmantic import ObjectId
from odmantic import query

from app.domain.entities import MLModel
from app.domain.entities import MLModelUpdate
from app.domain.entities import Pagination
from app.domain.errors import ModelNotFoundException
from app.domain.errors import PageNotFoundException
from app.domain.utils import get_next_page
from app.domain.utils import get_total_pages

LOGGER = logging.getLogger(__name__)


class ModelsUseCases:
    def __init__(
        self,
        engine: AIOEngine,
    ):
        self.engine = engine

    async def create_model(self, model: MLModel) -> MLModel:
        model = await self.engine.save(model)
        return model

    async def list_models(self, page: int, page_size: int) -> Pagination:
        count = await self.engine.count(MLModel)
        total_pages = get_total_pages(count, page_size)
        if page >= total_pages:
            raise PageNotFoundException()
        items = await self.engine.find(
            MLModel,
            skip=page * page_size,
            limit=page_size,
            sort=query.desc(MLModel.timestamp),
        )
        next_page = get_next_page(page, total_pages)
        return Pagination[MLModel](
            count=count, next_page=next_page, page=page, page_size=page_size, items=items
        )

    async def get_model_by_id(self, id: ObjectId) -> MLModel:
        model = await self.engine.find_one(MLModel, MLModel.id == id)
        if not model:
            raise ModelNotFoundException(id)
        return model

    async def update_model_by_id(self, id: ObjectId, patch: MLModelUpdate) -> MLModel:
        model = await self.engine.find_one(MLModel, MLModel.id == id)
        if model is None:
            raise ModelNotFoundException(id)
        model.update(patch)
        await self.engine.save(model)
        return model

    async def delete_model_by_id(self, id: ObjectId) -> MLModel:
        model = await self.engine.find_one(MLModel, MLModel.id == id)
        if model is None:
            raise ModelNotFoundException(id)
        await self.engine.delete(model)
        return model

    async def get_latest_model(self) -> MLModel:
        model = await self.engine.find_one(MLModel, sort=query.desc(MLModel.timestamp))
        return model

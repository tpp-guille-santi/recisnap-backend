import logging

from odmantic import AIOEngine
from odmantic import ObjectId
from odmantic import query

from app.domain.entities import MLModel
from app.domain.entities import MLModelUpdate
from app.domain.errors import ModelNotFoundException

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

    async def list_models(self) -> list[MLModel]:
        return await self.engine.find(MLModel, sort=query.desc(MLModel.timestamp))

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

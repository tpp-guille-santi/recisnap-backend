import aiofiles
from odmantic import ObjectId, query, AIOEngine

from domain.entities import MLModel, MLModelUpdate
from domain.errors import ModelNotFoundException, NoModelsFoundException
from domain.repositories import AbstractFirebaseStorageRepository


class ModelsUseCases:
    model_timestamp: int | None = None

    def __init__(self,
                 engine: AIOEngine,
                 firebase_storage_repository_dependency: AbstractFirebaseStorageRepository,
                 ):
        self.engine = engine
        self.firebase_storage_repository_dependency = firebase_storage_repository_dependency

    async def create_model(self, model: MLModel) -> MLModel:
        model = await self.engine.save(model)
        return model

    async def list_models(self, limit: int | None, name: str | None) -> list[MLModel]:
        query_filters = []
        if name:
            query_filters.append(MLModel.name == name)
        return await self.engine.find(MLModel,
                                      *query_filters,
                                      sort=query.desc(MLModel.timestamp),
                                      limit=limit)

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

    async def get_latest_model(self, model_name: str) -> MLModel:
        models = await self.list_models(limit=1, name=model_name)
        if not models:
            raise NoModelsFoundException()
        return models[0]

    async def get_model_file_directory(self, model_name: str):
        model = await self.get_latest_model(model_name)
        if ModelsUseCases.model_changed(model):
            await self.update_model_file(model)
        return f'./models/{model.name}.pt'

    async def update_model_file(self, model: MLModel):
        filename = f'{model.name}.pt'
        file_bytes = await self.firebase_storage_repository_dependency.get_model_file(filename)
        async with aiofiles.open(f'./models/{filename}', 'wb') as f:
            await f.write(file_bytes)
        ModelsUseCases.model_timestamp = model.timestamp

    @classmethod
    def model_changed(cls, model: MLModel):
        return cls.model_timestamp != model.timestamp

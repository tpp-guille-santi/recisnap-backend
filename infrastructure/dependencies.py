from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from domain.usecases.general_usecases import UseCases
from domain.usecases.materials_usecases import MaterialsUseCases
from domain.usecases.models_usecases import ModelsUseCases
from domain.usecases.pages_usecases import PagesUseCases
from domain.usecases.users_usecases import UsersUseCases
from infrastructure.repositories import FirebaseStorageRepository, GeorefRepository
from infrastructure.settings import MONGO_URL, DATABASE_NAME, FIREBASE_STORAGE_BASE_URL, \
    GEOREF_STORAGE_BASE_URL


def firebase_storage_repository_dependency() -> FirebaseStorageRepository:
    return FirebaseStorageRepository(FIREBASE_STORAGE_BASE_URL)


def georef_repository_dependency() -> GeorefRepository:
    return GeorefRepository(GEOREF_STORAGE_BASE_URL)


def engine_dependency() -> AIOEngine:
    client = AsyncIOMotorClient(MONGO_URL)
    return AIOEngine(client=client, database=DATABASE_NAME)


def usecases_dependency(
        engine: AIOEngine = Depends(engine_dependency),
) -> UseCases:
    return UseCases()


def users_usecases_dependency(
        engine: AIOEngine = Depends(engine_dependency),
) -> UsersUseCases:
    return UsersUseCases(engine)


def pages_usecases_dependency(
        engine: AIOEngine = Depends(engine_dependency),
        georef_repository: GeorefRepository = Depends(georef_repository_dependency)
) -> PagesUseCases:
    return PagesUseCases(engine, georef_repository)


def materials_usecases_dependency(
        engine: AIOEngine = Depends(engine_dependency),
) -> MaterialsUseCases:
    return MaterialsUseCases(engine)


def models_usecases_dependency(
        engine: AIOEngine = Depends(engine_dependency),
        firebase_storage_repository: FirebaseStorageRepository = Depends(
            firebase_storage_repository_dependency),
) -> ModelsUseCases:
    return ModelsUseCases(engine, firebase_storage_repository)

import certifi
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from domain.usecases.images_usecases import ImagesUseCases
from domain.usecases.instructions_usecases import InstructionsUseCases
from domain.usecases.materials_usecases import MaterialsUseCases
from domain.usecases.users_usecases import UsersUseCases
from infrastructure.repositories import DetaDriveRepository
from infrastructure.repositories import FirebaseAuthRepository
from infrastructure.repositories import FirebaseStorageRepository
from infrastructure.repositories import GeorefRepository
from infrastructure.settings import settings


def firebase_auth_repository_dependency() -> FirebaseAuthRepository:
    return FirebaseAuthRepository()


def firebase_storage_repository_dependency() -> FirebaseStorageRepository:
    return FirebaseStorageRepository(settings.FIREBASE_STORAGE_BASE_URL)


def deta_drive_repository_dependency() -> DetaDriveRepository:
    return DetaDriveRepository(settings.DETA_DRIVE_KEY, settings.DETA_DRIVE)


def georef_repository_dependency() -> GeorefRepository:
    return GeorefRepository(settings.GEOREF_BASE_URL)


def engine_dependency() -> AIOEngine:
    client = AsyncIOMotorClient(settings.MONGO_URL, tlsCAFile=certifi.where())
    return AIOEngine(client=client, database=settings.DATABASE_NAME)


# def usecases_dependency(
#     engine: AIOEngine = Depends(engine_dependency),
# ) -> UseCases:
#     return UseCases()


def users_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
    firebase_auth_repository: FirebaseAuthRepository = Depends(firebase_auth_repository_dependency),
) -> UsersUseCases:
    return UsersUseCases(engine, firebase_auth_repository)


def instructions_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
    georef_repository: GeorefRepository = Depends(georef_repository_dependency),
    deta_drive_repository: DetaDriveRepository = Depends(deta_drive_repository_dependency),
) -> InstructionsUseCases:
    return InstructionsUseCases(engine, georef_repository, deta_drive_repository)


def materials_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
) -> MaterialsUseCases:
    return MaterialsUseCases(engine)


def images_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
    deta_drive_repository: DetaDriveRepository = Depends(deta_drive_repository_dependency),
) -> ImagesUseCases:
    return ImagesUseCases(engine, deta_drive_repository)


# def models_usecases_dependency(
#         engine: AIOEngine = Depends(engine_dependency),
# ) -> ModelsUseCases:
#     return ModelsUseCases(engine)

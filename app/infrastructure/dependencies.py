import certifi
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.domain.usecases.images_usecases import ImagesUseCases
from app.domain.usecases.instructions_usecases import InstructionsUseCases
from app.domain.usecases.materials_usecases import MaterialsUseCases
from app.domain.usecases.models_usecases import ModelsUseCases
from app.domain.usecases.users_usecases import UsersUseCases
from app.infrastructure.repositories import DetaDriveRepository
from app.infrastructure.repositories import FirebaseAuthRepository
from app.infrastructure.repositories import FirebaseStorageRepository
from app.infrastructure.settings import settings


def firebase_auth_repository_dependency() -> FirebaseAuthRepository:
    return FirebaseAuthRepository()


def firebase_storage_repository_dependency() -> FirebaseStorageRepository:
    return FirebaseStorageRepository(settings.FIREBASE_STORAGE_BASE_URL)


def deta_drive_repository_dependency() -> DetaDriveRepository:
    return DetaDriveRepository(settings.DETA_DRIVE_KEY, settings.DETA_DRIVE)


def engine_dependency() -> AIOEngine:
    client = AsyncIOMotorClient(settings.MONGO_URL, tlsCAFile=certifi.where())
    return AIOEngine(client=client, database=settings.DATABASE_NAME)


def users_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
    firebase_auth_repository: FirebaseAuthRepository = Depends(firebase_auth_repository_dependency),
) -> UsersUseCases:
    return UsersUseCases(engine, firebase_auth_repository)


def instructions_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
    deta_drive_repository: DetaDriveRepository = Depends(deta_drive_repository_dependency),
) -> InstructionsUseCases:
    return InstructionsUseCases(engine, deta_drive_repository)


def materials_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
) -> MaterialsUseCases:
    return MaterialsUseCases(engine)


def images_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
    deta_drive_repository: DetaDriveRepository = Depends(deta_drive_repository_dependency),
) -> ImagesUseCases:
    return ImagesUseCases(engine, deta_drive_repository)


def models_usecases_dependency(
    engine: AIOEngine = Depends(engine_dependency),
) -> ModelsUseCases:
    return ModelsUseCases(engine)

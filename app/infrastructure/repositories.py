import logging

import httpx
from asyncer import asyncify
from deta import Deta
from deta.drive import DriveStreamingBody
from firebase_admin import auth

from app.domain.repositories import AbstractDetaDriveRepository
from app.domain.repositories import AbstractFirebaseAuthRepository
from app.domain.repositories import AbstractFirebaseStorageRepository

LOGGER = logging.getLogger(__name__)


class FirebaseStorageRepository(AbstractFirebaseStorageRepository):
    def __init__(self, firebase_storage_base_url: str):
        self.client = httpx.AsyncClient()
        self.firebase_storage_base_url = firebase_storage_base_url

    async def get_content(self, filename: str) -> bytes:
        r = await self.client.get(f'{self.firebase_storage_base_url}/models%2F{filename}?alt=media')
        return r.content


class DetaDriveRepository(AbstractDetaDriveRepository):
    def __init__(self, deta_project_key: str, deta_drive: str):
        self.deta_project_key = deta_project_key
        self.deta_drive = deta_drive

    async def upload_file(self, filename: str, file: bytes) -> None:
        deta = Deta(self.deta_project_key)
        drive = deta.Drive(self.deta_drive)
        await asyncify(drive.put)(filename, file)

    async def download_file(self, filename: str) -> DriveStreamingBody:
        deta = Deta(self.deta_project_key)
        drive = deta.Drive(self.deta_drive)
        file = await asyncify(drive.get)(filename)
        return file


class FirebaseAuthRepository(AbstractFirebaseAuthRepository):
    async def delete_user(self, firebase_uid: str) -> None:
        await asyncify(auth.delete_user)(uid=firebase_uid)

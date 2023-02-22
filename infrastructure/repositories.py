import httpx
from asyncer import asyncify
from firebase_admin import auth

from domain.entities import GeorefLocation
from domain.repositories import AbstractFirebaseAuthRepository
from domain.repositories import AbstractFirebaseStorageRepository
from domain.repositories import AbstractGeorefRepository


class FirebaseStorageRepository(AbstractFirebaseStorageRepository):
    def __init__(self, firebase_storage_base_url: str):
        self.client = httpx.AsyncClient()
        self.firebase_storage_base_url = firebase_storage_base_url

    async def get_content(self, filename: str) -> bytes:
        r = await self.client.get(f'{self.firebase_storage_base_url}/models%2F{filename}?alt=media')
        return r.content


class FirebaseAuthRepository(AbstractFirebaseAuthRepository):
    async def delete_user(self, firebase_uid: str) -> None:
        await asyncify(auth.delete_user)(uid=firebase_uid)


class GeorefRepository(AbstractGeorefRepository):
    def __init__(self, georef_base_url: str):
        self.client = httpx.AsyncClient()
        self.georef_base_url = georef_base_url

    async def get_georef_location(self, latitude: float, longitude: float) -> GeorefLocation:
        r = await self.client.get(f'{self.georef_base_url}lat={latitude}&lon={longitude}')
        return GeorefLocation(**r.json())

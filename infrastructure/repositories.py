import httpx

from domain.entities import GeorefLocation
from domain.repositories import AbstractFirebaseStorageRepository, AbstractGeorefRepository


class FirebaseStorageRepository(AbstractFirebaseStorageRepository):

    def __init__(self, firebase_storage_base_url: str):
        self.client = httpx.AsyncClient()
        self.firebase_storage_base_url = firebase_storage_base_url

    async def get_model_file(self, filename: str) -> bytes:
        r = await self.client.get(f'{self.firebase_storage_base_url}/models%2F{filename}?alt=media')
        return r.content


class GeorefRepository(AbstractGeorefRepository):
    def __init__(self, georef_base_url: str):
        self.client = httpx.AsyncClient()
        self.georef_base_url = georef_base_url

    async def get_georef_location(self, latitude: float, longitude: float) -> GeorefLocation:
        r = await self.client.get(f'{self.georef_base_url}lat={latitude}&lon={longitude}')
        return GeorefLocation(**r.json())

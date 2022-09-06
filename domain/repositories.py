from abc import ABC, abstractmethod

from domain.entities import GeorefLocation


class AbstractFirebaseStorageRepository(ABC):

    @abstractmethod
    async def get_model_file(self, filename: str) -> bytes:
        raise NotImplementedError


class AbstractGeorefRepository(ABC):
    @abstractmethod
    async def get_georef_location(self, latitude: float, longitude: float) -> GeorefLocation:
        raise NotImplementedError
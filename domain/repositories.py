from abc import ABC
from abc import abstractmethod

from domain.entities import GeorefLocation


class AbstractFirebaseAuthRepository(ABC):
    @abstractmethod
    async def delete_user(self, firebase_uid: str) -> None:
        raise NotImplementedError


class AbstractFirebaseStorageRepository(ABC):
    @abstractmethod
    async def get_content(self, filename: str) -> bytes:
        raise NotImplementedError


class AbstractGeorefRepository(ABC):
    @abstractmethod
    async def get_georef_location(self, latitude: float, longitude: float) -> GeorefLocation:
        raise NotImplementedError

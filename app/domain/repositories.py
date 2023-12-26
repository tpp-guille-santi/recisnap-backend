from abc import ABC
from abc import abstractmethod

from deta.drive import DriveStreamingBody


class AbstractFirebaseAuthRepository(ABC):
    @abstractmethod
    async def delete_user(self, firebase_uid: str) -> None:
        raise NotImplementedError


class AbstractFirebaseStorageRepository(ABC):
    @abstractmethod
    async def get_content(self, filename: str) -> bytes:
        raise NotImplementedError


class AbstractDetaDriveRepository(ABC):
    @abstractmethod
    async def upload_file(self, filename: str, file: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def download_file(self, filename: str) -> DriveStreamingBody:
        raise NotImplementedError

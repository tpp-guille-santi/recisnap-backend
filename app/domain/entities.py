from typing import Generic
from typing import TypeVar

from fastapi import Query
from odmantic import Model
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

T = TypeVar('T')


class User(Model):
    firebase_uid: str
    name: str
    email: EmailStr
    permissions: list[str] = []


class Pagination(BaseModel, Generic[T]):
    count: int
    next_page: int | None
    page: int
    page_size: int
    items: list[T]


class UserUpdate(BaseModel):
    permissions: list[str] | None = None
    name: str | None = None
    email: EmailStr | None = None


class Material(Model):
    name: str
    order: int
    enabled: bool


class MaterialUpdate(BaseModel):
    name: str | None = None
    order: int | None = None
    enabled: bool | None = None


class MLModel(Model):
    timestamp: int
    accuracy: float


class MLModelUpdate(BaseModel):
    timestamp: int | None = None
    accuracy: float | None = None


class GeoJSON(BaseModel):
    type: str = 'Point'
    coordinates: tuple[float, float] | None = None


class Instruction(Model):
    material_name: str
    editable: bool
    lat: float
    lon: float
    geo_json: GeoJSON


class InstructionSearch(BaseModel):
    material_name: str | None = None
    lat: float
    lon: float
    max_distance: float


class InstructionCreate(BaseModel):
    material_name: str
    editable: bool
    lat: float
    lon: float


class InstructionUpdate(BaseModel):
    material_name: str | None = None
    editable: bool | None = None


class Image(Model):
    filename: str
    material_name: str
    downloaded: bool = False
    tags: list[str] = []


class ImageSearch(BaseModel):
    filename: str | None = None
    material_name: str | None = None
    downloaded: bool | None = None
    tags: list[str] | None = Field(Query(default=None))


class ImageUpdate(BaseModel):
    downloaded: bool | None = None

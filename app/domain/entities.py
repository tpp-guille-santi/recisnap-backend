from typing import Union

from odmantic import Model
from pydantic import BaseModel
from pydantic import EmailStr


class User(Model):
    firebase_uid: str
    name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    permissions: Union[list[str], None] = ['view_instructions']


class UserUpdate(BaseModel):
    name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    permissions: Union[list[str], None] = None


class Material(Model):
    name: str
    order: int
    enabled: bool


class MaterialUpdate(BaseModel):
    name: Union[str, None] = None
    order: Union[int, None] = None
    enabled: Union[bool, None] = None


class MaterialPrediction(Model):
    image_id: str
    name: str
    tags: Union[list[str], None] = None


class MLModel(Model):
    name: str
    timestamp: int


class MLModelUpdate(BaseModel):
    name: Union[str, None] = None
    timestamp: Union[int, None] = None


class GeoJSON(BaseModel):
    type: Union[str, None] = 'Point'
    coordinates: Union[tuple[float, float], None]


class Instruction(Model):
    material_name: str
    editable: bool
    lat: float
    lon: float
    geo_json: GeoJSON
    provincia: Union[str, None]
    departamento: Union[str, None]
    municipio: Union[str, None]


class InstructionSearch(BaseModel):
    material_name: Union[str, None] = None
    lat: float
    lon: float
    max_distance: float


class InstructionCreate(BaseModel):
    material_name: str
    editable: bool
    lat: float
    lon: float


class InstructionUpdate(BaseModel):
    material_name: Union[str, None]
    editable: Union[bool, None]


class GeorefLugar(BaseModel):
    id: Union[str, None]
    nombre: Union[str, None]


class GeorefParametros(BaseModel):
    lat: float
    lon: float


class GeorefUbicacion(BaseModel):
    provincia: Union[GeorefLugar, None]
    departamento: Union[GeorefLugar, None]
    municipio: Union[GeorefLugar, None]
    lat: float
    lon: float


class GeorefLocation(BaseModel):
    parametros: GeorefParametros
    ubicacion: GeorefUbicacion


class Image(Model):
    filename: str
    material_name: str
    downloaded: bool = False
    tags: Union[list[str], None] = None


class ImageSearch(BaseModel):
    filename: Union[str, None] = None
    material_name: Union[str, None] = None
    downloaded: Union[bool, None] = None
    tags: Union[list[str], None] = None


class ImageUpdate(BaseModel):
    downloaded: Union[bool, None] = None

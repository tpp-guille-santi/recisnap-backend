from odmantic import Model
from pydantic import BaseModel
from pydantic import EmailStr


class User(Model):
    firebase_uid: str
    name: str | None = None
    email: EmailStr | None = None
    permissions: list[str] | None = ['view_instructions']


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    permissions: list[str] | None = None


class Material(Model):
    name: str
    order: int
    enabled: bool


class MaterialUpdate(BaseModel):
    name: str | None = None
    order: int | None = None
    enabled: bool | None = None


class MaterialPrediction(Model):
    image_id: str
    name: str
    tags: list[str] | None = None


class MLModel(Model):
    name: str
    timestamp: int


class MLModelUpdate(BaseModel):
    name: str | None = None
    timestamp: int | None = None


class GeoJSON(BaseModel):
    type: str | None = 'Point'
    coordinates: tuple[float, float] | None


class Instruction(Model):
    material_name: str
    editable: bool
    lat: float
    lon: float
    geo_json: GeoJSON
    provincia: str | None
    departamento: str | None
    municipio: str | None


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
    material_name: str | None
    editable: bool | None


class GeorefLugar(BaseModel):
    id: str | None
    nombre: str | None


class GeorefParametros(BaseModel):
    lat: float
    lon: float


class GeorefUbicacion(BaseModel):
    provincia: GeorefLugar | None
    departamento: GeorefLugar | None
    municipio: GeorefLugar | None
    lat: float
    lon: float


class GeorefLocation(BaseModel):
    parametros: GeorefParametros
    ubicacion: GeorefUbicacion

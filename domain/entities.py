from urllib.parse import quote_plus

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


class Instruction(Model):
    material_name: str
    editable: bool
    municipio: str | None
    provincia: str | None
    departamento: str | None


class InstructionSearch(BaseModel):
    material_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    municipio: str | None = None
    provincia: str | None = None
    departamento: str | None = None


class InstructionUpdate(BaseModel):
    material_name: str | None
    editable: bool | None
    municipio: str | None
    provincia: str | None
    departamento: str | None


class BackofficeInstructionRequest(BaseModel):
    material_name: str


class InstructionResponse(BaseModel):
    id: str
    material_name: str
    editable: bool
    url: str | None
    municipio: str | None
    provincia: str | None
    departamento: str | None

    @staticmethod
    def from_entity(
        instruction: Instruction, firebase_storage_base_url: str
    ) -> 'InstructionResponse':
        return InstructionResponse(
            id=str(instruction.id),
            material_name=instruction.material_name,
            editable=instruction.editable,
            url=_generate_url(instruction, firebase_storage_base_url),
            municipio=instruction.municipio,
            provincia=instruction.provincia,
            departamento=instruction.departamento,
        )


def _generate_url(instruction: Instruction, firebase_storage_base_url: str) -> str | None:
    path = quote_plus(
        f'instructions/{str(instruction.provincia)}/{str(instruction.municipio)}/{str(instruction.departamento)}/{str(instruction.provincia)}-{str(instruction.municipio)}-{str(instruction.departamento)}-{instruction.material_name}.md'
    )
    return f'{firebase_storage_base_url}/{path}?alt=media'


class GeorefLugar(BaseModel):
    id: str | None
    nombre: str | None


class GeorefParametros(BaseModel):
    lat: float
    lon: float


class GeorefUbicacion(BaseModel):
    departamento: GeorefLugar
    municipio: GeorefLugar
    provincia: GeorefLugar
    lat: float
    lon: float


class GeorefLocation(BaseModel):
    parametros: GeorefParametros
    ubicacion: GeorefUbicacion

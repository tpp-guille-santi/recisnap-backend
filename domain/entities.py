from urllib.parse import quote_plus

from odmantic import Model
from pydantic import BaseModel, EmailStr


class User(Model):
    firebase_uid: str
    name: str | None = None
    email: EmailStr | None = None
    permissions: list[str] | None = None


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


class Page(Model):
    material_name: str
    editable: bool
    municipio: str | None
    provincia: str | None
    departamento: str | None


class PageSearch(BaseModel):
    material_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    municipio: str | None = None
    provincia: str | None = None
    departamento: str | None = None


class PageUpdate(BaseModel):
    material_name: str | None
    editable: bool | None
    municipio: str | None
    provincia: str | None
    departamento: str | None


class BackofficePageRequest(BaseModel):
    material_name: str


class PageResponse(BaseModel):
    id: str
    material_name: str
    editable: bool
    url: str | None
    municipio: str | None
    provincia: str | None
    departamento: str | None

    @staticmethod
    def from_entity(page: Page, firebase_storage_base_url: str) -> "PageResponse":
        return PageResponse(
            id=str(page.id),
            material_name=page.material_name,
            editable=page.editable,
            url=generate_url(page, firebase_storage_base_url),
            municipio=page.municipio,
            provincia=page.provincia,
            departamento=page.departamento,
        )


def generate_url(page: Page, firebase_storage_base_url: str) -> str | None:
    path = quote_plus(
        f'pages/{str(page.provincia)}/{str(page.municipio)}/{str(page.departamento)}/{str(page.provincia)}-{str(page.municipio)}-{str(page.departamento)}-{page.material_name}.md')
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

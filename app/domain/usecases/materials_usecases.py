import logging

from odmantic import AIOEngine
from odmantic import ObjectId
from odmantic import query

from app.domain.entities import Material
from app.domain.entities import MaterialUpdate
from app.domain.entities import Pagination
from app.domain.errors import MaterialNotFoundException
from app.domain.errors import PageNotFoundException
from app.domain.utils import get_next_page
from app.domain.utils import get_total_pages

LOGGER = logging.getLogger(__name__)


class MaterialsUseCases:
    def __init__(self, engine: AIOEngine):
        self.engine = engine

    async def create_material(self, material: Material) -> Material:
        await self.engine.save(material)
        return material

    async def list_materials(self, page: int, page_size: int, enabled: bool | None) -> Pagination:
        query_filters = []
        if enabled is not None:
            query_filters.append(Material.enabled == enabled)
        count = await self.engine.count(Material, *query_filters)
        total_pages = get_total_pages(count, page_size)
        if page >= total_pages:
            raise PageNotFoundException()
        entities = await self.engine.find(
            Material,
            *query_filters,
            skip=page * page_size,
            limit=page_size,
            sort=Material.order,
        )
        next_page = get_next_page(page, total_pages)
        return Pagination(
            count=count, next_page=next_page, page=page, page_size=page_size, entities=entities
        )

    async def get_material_by_id(self, id: ObjectId) -> Material:
        material = await self.engine.find_one(Material, Material.id == id)
        if not material:
            raise MaterialNotFoundException(id)
        return material

    async def update_material_by_id(self, id: ObjectId, patch: MaterialUpdate) -> Material:
        material = await self.engine.find_one(Material, Material.id == id)
        if material is None:
            raise MaterialNotFoundException(id)
        material.update(patch)
        await self.engine.save(material)
        return material

    async def delete_material_by_id(self, id: ObjectId) -> Material:
        material = await self.engine.find_one(Material, Material.id == id)
        if material is None:
            raise MaterialNotFoundException(id)
        await self.engine.delete(material)
        return material

    async def get_latest_material(self) -> Material:
        material = await self.engine.find_one(Material, sort=query.desc(Material.order))
        return material

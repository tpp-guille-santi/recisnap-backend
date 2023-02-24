import logging
from typing import Union

from odmantic import AIOEngine
from odmantic import ObjectId

from domain.entities import Material
from domain.entities import MaterialUpdate
from domain.errors import MaterialNotFoundException

LOGGER = logging.getLogger(__name__)


class MaterialsUseCases:
    def __init__(self, engine: AIOEngine):
        self.engine = engine

    async def create_material(self, material: Material) -> Material:
        await self.engine.save(material)
        return material

    async def list_materials(self, enabled: Union[bool, None]) -> list[Material]:
        query_filters = []
        if enabled is not None:
            query_filters.append(Material.enabled == enabled)
        return await self.engine.find(Material, *query_filters, sort=Material.order)

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

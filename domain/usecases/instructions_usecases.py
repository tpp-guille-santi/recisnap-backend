import logging

from odmantic import AIOEngine
from odmantic import ObjectId

from domain.entities import GeoJSON
from domain.entities import Instruction
from domain.entities import InstructionCreate
from domain.entities import InstructionSearch
from domain.entities import InstructionUpdate
from domain.errors import InstructionNotFoundException
from infrastructure.repositories import GeorefRepository

LOGGER = logging.getLogger(__name__)


class InstructionsUseCases:
    def __init__(self, engine: AIOEngine, georef_repository: GeorefRepository):
        self.engine = engine
        self.georef_repository = georef_repository

    async def create_instruction(self, create: InstructionCreate) -> Instruction:
        georef_location = await self.georef_repository.get_georef_location(create.lat, create.lon)
        ubicacion = georef_location.ubicacion
        provincia = ubicacion.provincia.nombre if ubicacion.provincia else None
        departamento = ubicacion.departamento.nombre if ubicacion.departamento else None
        municipio = ubicacion.municipio.nombre if ubicacion.municipio else None
        geo_json = GeoJSON(coordinates=(create.lon, create.lat))
        instruction = Instruction(
            material_name=create.material_name,
            editable=create.editable,
            lat=create.lat,
            lon=create.lon,
            geo_json=geo_json,
            municipio=municipio,
            provincia=provincia,
            departamento=departamento,
        )
        return await self.engine.save(instruction)

    async def list_instructions(self) -> list[Instruction]:
        return await self.engine.find(Instruction)

    async def search_instructions(self, search: InstructionSearch):
        # This is the ideal code, but as it doesn't work, we are using a workaround
        # query_filters = self._generate_query_filters(search)
        # return await self.engine.find(Instruction, query_filters)
        collection = self.engine.get_collection(Instruction)
        query_filters = self._generate_query_filters(search)
        response = collection.find(query_filters)
        instructions = await response.to_list(length=None)
        return [Instruction(**instruction) for instruction in instructions]

    @staticmethod
    def _generate_query_filters(search: InstructionSearch) -> dict:
        query_filters = {
            'geo_json': {
                '$near': {
                    '$geometry': {'type': 'Point', 'coordinates': [search.lon, search.lat]},
                    '$maxDistance': search.max_distance,
                }
            }
        }
        if search.material_name:
            query_filters['material_name'] = {'$eq': search.material_name}
        return query_filters

    # @staticmethod
    # def _generate_query_filters(self, search: InstructionSearch) -> list[dict]:
    #     query_filters = [
    #         {
    #             'geo_json': {
    #                 '$near': {
    #                     '$geometry': {'type': 'Point', 'coordinates': [search.lon, search.lat]},
    #                     '$maxDistance': search.max_distance,
    #                 }
    #             }
    #         }
    #     ]
    #     if search.material_name:
    #         query_filters.append(Instruction.material_name == search.material_name)
    #     return query_filters

    async def get_instruction_by_id(self, id: ObjectId) -> Instruction:
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        if not instruction:
            raise InstructionNotFoundException(id)
        return instruction

    async def update_instruction_by_id(self, id: ObjectId, patch: InstructionUpdate) -> Instruction:
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        if instruction is None:
            raise InstructionNotFoundException(id)
        instruction.update(patch)
        await self.engine.save(instruction)
        return instruction

    async def delete_instruction_by_id(self, id: ObjectId) -> Instruction:
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        if instruction is None:
            raise InstructionNotFoundException(id)
        await self.engine.delete(instruction)
        return instruction

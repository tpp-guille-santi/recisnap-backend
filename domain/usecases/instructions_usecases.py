import logging

from odmantic import AIOEngine
from odmantic import ObjectId

from domain.entities import Instruction
from domain.entities import InstructionSearch
from domain.entities import InstructionUpdate
from domain.errors import InstructionNotFoundException
from infrastructure.repositories import GeorefRepository

LOGGER = logging.getLogger(__name__)


class InstructionsUseCases:
    def __init__(self, engine: AIOEngine, georef_repository: GeorefRepository):
        self.engine = engine
        self.georef_repository = georef_repository

    async def create_instruction(self, instruction: Instruction) -> Instruction:
        instruction = await self.engine.save(instruction)
        return instruction

    async def list_instructions(self) -> list[Instruction]:
        return await self.engine.find(Instruction)

    async def search_instructions(self, search: InstructionSearch) -> list[Instruction]:
        query_filters = await self._generate_query_filters(search)
        return await self.engine.find(Instruction, *query_filters)

    async def _generate_query_filters(self, search: InstructionSearch) -> list[bool]:
        query_filters = []
        if search.latitude and search.longitude:
            georef_location = await self.georef_repository.get_georef_location(
                search.latitude, search.longitude
            )
            query_filters.append(
                Instruction.provincia == georef_location.ubicacion.provincia.nombre
            )
            query_filters.append(
                Instruction.municipio == georef_location.ubicacion.municipio.nombre
            )
            query_filters.append(
                Instruction.departamento == georef_location.ubicacion.departamento.nombre
            )
            return query_filters
        if search.material_name:
            query_filters.append(Instruction.material_name == search.material_name)
        if search.provincia:
            query_filters.append(Instruction.provincia == search.provincia)
        if search.municipio:
            query_filters.append(Instruction.municipio == search.municipio)
        if search.departamento:
            query_filters.append(Instruction.departamento == search.departamento)
        return query_filters

    async def get_instruction_by_id(self, id: ObjectId) -> Instruction:
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        if not instruction:
            raise InstructionNotFoundException(id)
        return instruction

    # async def get_instruction_by_georef(self, id: ObjectId, app_instruction_request: AppInstructionRequest) -> Instruction:
    #     georef_location = await self.georef_repository.get_georef_location(app_instruction_request)
    #     instruction = await self.engine.find_one(
    #         Instruction,
    #         (Instruction.departamento == georef_location.ubicacion.departamento.nombre) &
    #         (Instruction.municipio == georef_location.ubicacion.municipio.nombre) &
    #         (Instruction.provincia == georef_location.ubicacion.provincia.nombre))
    #     if not instruction:
    #         raise InstructionNotFoundException(id)
    #     return instruction

    # async def get_instructions_by_lat_long(self, id: ObjectId, app_instruction_request: AppInstructionRequest) -> Instruction:
    #     georef_location = await self.georef_repository.get_georef_location(app_instruction_request)
    #     instruction = await self.engine.find_one(
    #         Instruction,
    #         (Instruction.departamento.id == georef_location.ubicacion.departamento.id) &
    #         (Instruction.municipio.id == georef_location.ubicacion.municipio.id) &
    #         (Instruction.provincia.id == georef_location.ubicacion.provincia.id))
    #     if not instruction:
    #         raise InstructionNotFoundException(id)
    #     return instruction

    async def update_instruction_by_id(self, id: ObjectId, patch: InstructionUpdate) -> Instruction:
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        if instruction is None:
            raise InstructionNotFoundException(id)
        instruction.update(patch)
        await self.engine.save(instruction)
        return instruction

    async def delete_instruction_by_id(self, id: ObjectId) -> Instruction:
        LOGGER.info('Here 1')
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        LOGGER.info('Here 2')
        if instruction is None:
            LOGGER.info('Here 3')
            raise InstructionNotFoundException(id)
        LOGGER.info('Here 4')
        await self.engine.delete(instruction)
        LOGGER.info('Here 5')
        return instruction

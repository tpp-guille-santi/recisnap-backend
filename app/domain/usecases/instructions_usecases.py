import logging

from odmantic import AIOEngine
from odmantic import ObjectId

from app.domain.entities import GeoJSON
from app.domain.entities import Instruction
from app.domain.entities import InstructionCreate
from app.domain.entities import InstructionSearch
from app.domain.entities import InstructionUpdate
from app.domain.entities import Pagination
from app.domain.errors import InstructionNotFoundException
from app.domain.errors import PageNotFoundException
from app.domain.repositories import AbstractDetaDriveRepository
from app.domain.utils import get_next_page
from app.domain.utils import get_total_pages

LOGGER = logging.getLogger(__name__)


class InstructionsUseCases:
    def __init__(
        self,
        engine: AIOEngine,
        deta_drive_repository: AbstractDetaDriveRepository,
    ):
        self.engine = engine
        self.deta_drive_repository = deta_drive_repository

    async def create_instruction(self, create: InstructionCreate) -> Instruction:
        geo_json = GeoJSON(coordinates=(create.lon, create.lat))
        instruction = Instruction(
            material_name=create.material_name,
            editable=create.editable,
            lat=create.lat,
            lon=create.lon,
            geo_json=geo_json,
        )
        return await self.engine.save(instruction)

    async def list_instructions(self, page: int, page_size: int) -> Pagination:
        count = await self.engine.count(Instruction)
        total_pages = get_total_pages(count, page_size)
        if page >= total_pages:
            raise PageNotFoundException()
        entities = await self.engine.find(
            Instruction,
            skip=page * page_size,
            limit=page_size,
        )
        next_page = get_next_page(page, total_pages)
        return Pagination(
            count=count, next_page=next_page, page=page, page_size=page_size, entities=entities
        )

    async def search_instructions(self, search: InstructionSearch) -> list[Instruction]:
        # This is the ideal code, but as it doesn't work, we are using a workaround
        # query_filters = self._generate_query_filters(search)
        # return await self.engine.find(Instruction, query_filters)
        collection = self.engine.get_collection(Instruction)
        query_filters = self._generate_query_filters(search)
        response = collection.find(query_filters)
        instructions = await response.to_list(length=None)
        return [Instruction.parse_doc(instruction) for instruction in instructions]

    @staticmethod
    def _generate_query_filters(search: InstructionSearch) -> dict:
        query_filters = {
            'geo_json': {
                '$geoNear': {
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

    async def upload_file(self, id: ObjectId, file: bytes) -> None:
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        if not instruction:
            raise InstructionNotFoundException(id)
        filename = f'{str(id)}.md'
        await self.deta_drive_repository.upload_file(filename, file)

    async def download_file(self, id: ObjectId):
        instruction = await self.engine.find_one(Instruction, Instruction.id == id)
        if not instruction:
            raise InstructionNotFoundException(id)
        filename = f'{str(id)}.md'
        return await self._download_file(filename)

    async def download_template(self):
        filename = 'template.md'
        return await self._download_file(filename)

    async def _download_file(self, filename):
        file = await self.deta_drive_repository.download_file(filename)
        return file.iter_chunks()

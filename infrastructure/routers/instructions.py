import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Response
from fastapi import status
from fastapi.responses import StreamingResponse
from odmantic import ObjectId

from domain.entities import Instruction
from domain.entities import InstructionCreate
from domain.entities import InstructionSearch
from domain.entities import InstructionUpdate
from domain.usecases.instructions_usecases import InstructionsUseCases
from infrastructure.dependencies import instructions_usecases_dependency

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix='/instructions',
    tags=['instructions'],
)


@router.post('/', response_model=Instruction, status_code=status.HTTP_201_CREATED)
async def create_instruction(
    instruction: InstructionCreate,
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    instruction = await instructions_usecases.create_instruction(instruction)
    return instruction


@router.get('/', response_model=list[Instruction])
async def list_instructions(
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    instructions = await instructions_usecases.list_instructions()
    return instructions


@router.post('/search/', response_model=list[Instruction])
async def search_instructions(
    search: InstructionSearch,
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    instructions = await instructions_usecases.search_instructions(search)
    return instructions


@router.get('/{id}/', response_model=Instruction)
async def get_instruction_by_id(
    id: ObjectId,
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    instruction = await instructions_usecases.get_instruction_by_id(id)
    return instruction


@router.patch('/{id}/', response_model=Instruction)
async def update_instruction_by_id(
    id: ObjectId,
    patch: InstructionUpdate,
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    instruction = await instructions_usecases.update_instruction_by_id(id, patch)
    return instruction


@router.delete('/{id}/', response_model=Instruction)
async def delete_instruction_by_id(
    id: ObjectId,
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    instruction = await instructions_usecases.delete_instruction_by_id(id)
    return instruction


@router.post('/{id}/markdown/')
async def upload_instruction_markdown(
    id: ObjectId,
    file: bytes = File(),
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    await instructions_usecases.upload_file(id, file)
    return Response()


@router.get('/{id}/markdown/')
async def download_instruction_markdown(
    id: ObjectId,
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    file = await instructions_usecases.download_file(id)
    return StreamingResponse(content=file, media_type='text/plain')


@router.get('/markdown/template/')
async def download_instructions_template_markdown(
    instructions_usecases: InstructionsUseCases = Depends(instructions_usecases_dependency),
):
    file = await instructions_usecases.download_template()
    return StreamingResponse(content=file, media_type='text/plain')

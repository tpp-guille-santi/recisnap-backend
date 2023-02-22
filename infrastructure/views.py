# LOGGER = logging.getLogger(__name__)
#
# router = APIRouter(tags=['test'])
# async def _get_image(file: UploadFile):
#     try:
#         image_bytes = await file.read()
#         image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
#         image.verify()
#         return Image.open(io.BytesIO(image_bytes)).convert('RGB')
#     except Exception:
#         raise FileTypeExceptionException()
# @router.post('/images')
# async def predict_material(
#         model_name: str = DEFAULT_MODEL,
#         image: Image = Depends(_get_image),
#         usecases: UseCases = Depends(usecases_dependency),
#         materials_usecases: MaterialsUseCases = Depends(materials_usecases_dependency),
#         models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     material = await usecases.predict_material(image, model_name, materials_usecases,
#                                                models_usecases)
#     return material
# @router.post('/models', response_model=MLModel, status_code=status.HTTP_201_CREATED)
# async def create_model(
#         model: MLModel, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     model = await models_usecases.create_model(model)
#     return model
#
#
# @router.get('/models', response_model=list[MLModel])
# async def list_models(
#         limit: int | None = None,
#         name: str | None = None,
#         models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
# ):
#     models = await models_usecases.list_models(limit, name)
#     return models
#
#
# @router.get('/models/{id}', response_model=MLModel)
# async def get_model_by_id(
#         id: ObjectId, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     model = await models_usecases.get_model_by_id(id)
#     return model
#
#
# @router.patch('/models/{id}', response_model=MLModel)
# async def update_model_by_id(
#         id: ObjectId,
#         patch: MLModelUpdate,
#         models_usecases: ModelsUseCases = Depends(models_usecases_dependency),
# ):
#     model = await models_usecases.update_model_by_id(id, patch)
#     return model
#
#
# @router.delete('/models/{id}', response_model=MLModel)
# async def delete_model_by_id(
#         id: ObjectId, models_usecases: ModelsUseCases = Depends(models_usecases_dependency)
# ):
#     model = await models_usecases.delete_model_by_id(id)
#     return model

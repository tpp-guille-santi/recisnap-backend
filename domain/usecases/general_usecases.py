import logging

import torch
from PIL.Image import Image
from torchvision.transforms import transforms
from tpp_guille_santi_commons.entities import MyModel

from domain.entities import Material
from domain.usecases.materials_usecases import MaterialsUseCases
from domain.usecases.models_usecases import ModelsUseCases

LOGGER = logging.getLogger(__name__)


class UseCases:

    async def predict_material(self, image: Image, model_name: str,
                               materials_usecases: MaterialsUseCases,
                               models_usecases: ModelsUseCases) -> Material:
        LOGGER.info('predict_material')
        image_transforms = transforms.Compose([
            transforms.CenterCrop(224),
            transforms.ToTensor()])
        image_tensor = image_transforms(image)
        image_tensor.unsqueeze_(0)
        if torch.cuda.is_available():
            image_tensor = image_tensor.cuda()
        model = MyModel()
        model_filename = await models_usecases.get_model_file_directory(model_name)
        model.load_state_dict(torch.load(model_filename,
                                         map_location=torch.device('cpu')))
        model.eval()
        output = model(image_tensor)
        _, class_idx = torch.max(output, dim=1)
        materials = await materials_usecases.list_materials(enabled=True)
        return materials[class_idx]

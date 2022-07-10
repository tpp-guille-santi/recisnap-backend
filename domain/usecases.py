import logging

import aiofiles
import torch
from PIL import Image
from torchvision import transforms

from domain.entities import Material, MyModel

LOGGER = logging.getLogger(__name__)

use_cuda = torch.cuda.is_available()


class UseCases:

    def __init__(self, model_location: str, model_names_location: str):
        self.model_location = model_location
        self.model_names_location = model_names_location

    async def predict_material(self, image: Image) -> Material:
        image_transforms = transforms.Compose([
            transforms.CenterCrop(224),
            transforms.ToTensor()])
        image_tensor = image_transforms(image)
        image_tensor.unsqueeze_(0)
        if use_cuda:
            image_tensor = image_tensor.cuda()
        model = MyModel()
        model.load_state_dict(torch.load(self.model_location, map_location=torch.device('cpu')))
        model.eval()
        output = model(image_tensor)
        _, class_idx = torch.max(output, dim=1)
        return await self._select_material(class_idx)

    async def _select_material(self, class_idx) -> Material:
        async with aiofiles.open(self.model_names_location, mode='r') as f:
            class_names = await f.readlines()
            class_names = [class_name[:-1] for class_name in class_names]
            material = class_names[class_idx]
            return Material(material=material)

    async def get_materials(self) -> list[Material]:
        async with aiofiles.open(self.model_names_location, mode='r') as f:
            class_names = await f.readlines()
            class_names = [class_name[:-1] for class_name in class_names]
            return [Material(material=class_name) for class_name in class_names]

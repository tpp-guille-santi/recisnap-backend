import logging

import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps

from domain.entities import Material
from domain.usecases.materials_usecases import MaterialsUseCases
from domain.usecases.models_usecases import ModelsUseCases
from infrastructure.settings import IMAGE_SIZE

LOGGER = logging.getLogger(__name__)


class UseCases:

    async def predict_material(self, image: Image, model_name: str,
                               materials_usecases: MaterialsUseCases,
                               models_usecases: ModelsUseCases) -> Material:
        LOGGER.info('predict_material_tensorflow')
        materials = await materials_usecases.list_materials(enabled=True)
        model = await models_usecases.get_loaded_model(model_name)
        image = ImageOps.fit(image, IMAGE_SIZE)
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        return materials[np.argmax(score)]

    # async def predict_material_tflite(self, image: Image, model_name: str,
    #                                   materials_usecases: MaterialsUseCases,
    #                                   models_usecases: ModelsUseCases) -> Material:
    #     LOGGER.info('predict_material_tensorflow')
    #     model_filename = await models_usecases.get_model_file_directory(model_name)
    #     interpreter = Interpreter(model_path=model_filename)
    #     interpreter.allocate_tensors()
    #     classify_lite = interpreter.get_signature_runner()
    #     data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    #     size = (224, 224)
    #     image = ImageOps.fit(image, size, Image.ANTIALIAS)
    #     image_array = np.asarray(image)
    #     normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    #     data[0] = normalized_image_array
    #     predictions_lite = classify_lite(sequential_1_input=data)['outputs']
    #     prediction = np.argmax(predictions_lite, axis=-1)
    #     materials = await materials_usecases.list_materials(enabled=True)
    #     return materials[prediction[0]]
    #
    # async def predict_material_tflite_2(self, image: Image, model_name: str,
    #                                   materials_usecases: MaterialsUseCases,
    #                                   models_usecases: ModelsUseCases) -> Material:
    #     LOGGER.info('predict_material_tensorflow')
    #     model_filename = await models_usecases.get_model_file_directory(model_name)
    #     interpreter = Interpreter(model_path=model_filename)
    #
    #     interpreter.allocate_tensors()
    #     input_details = interpreter.get_input_details()
    #     print(input_details)
    #     size = (224, 224)
    #     image = ImageOps.fit(image, size, Image.ANTIALIAS)
    #     # Preprocess the image to required size and cast
    #     img_array = tf.keras.utils.img_to_array(image)
    #     img_array = tf.expand_dims(img_array, 0)
    #     input_index = interpreter.get_input_details()[0]["index"]
    #     interpreter.set_tensor(input_index, img_array)
    #     interpreter.invoke()
    #     output_details = interpreter.get_output_details()
    #     output_data = interpreter.get_tensor(output_details[0]['index'])
    #     pred = np.squeeze(output_data)
    #     prediction = np.argmax(pred, axis=-1)
    #     materials = await materials_usecases.list_materials(enabled=True)
    #     return materials[prediction[0]]

    # async def predict_material_pytorch(self, image: Image, model_name: str,
    #                            materials_usecases: MaterialsUseCases,
    #                            models_usecases: ModelsUseCases) -> Material:
    #     LOGGER.info('predict_material')
    #     image_transforms = transforms.Compose([
    #         transforms.CenterCrop(224),
    #         transforms.ToTensor()])
    #     image_tensor = image_transforms(image)
    #     image_tensor.unsqueeze_(0)
    #     if torch.cuda.is_available():
    #         image_tensor = image_tensor.cuda()
    #     model = MyModel()
    #     model_filename = await models_usecases.get_model_file_directory(model_name)
    #     model.load_state_dict(torch.load(model_filename,
    #                                      map_location=torch.device('cpu')))
    #     model.eval()
    #     output = model(image_tensor)
    #     _, class_idx = torch.max(output, dim=1)
    #     materials = await materials_usecases.list_materials(enabled=True)
    #     return materials[class_idx]

    # async def predict_material_tensorflow(self, image: Image, model_name: str,
    #                                       materials_usecases: MaterialsUseCases,
    #                                       models_usecases: ModelsUseCases) -> Material:
    #     LOGGER.info('predict_material_tensorflow')
    #     model = await models_usecases.get_loaded_model(model_name)
    #     data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    #     size = (224, 224)
    #     image = ImageOps.fit(image, size, Image.ANTIALIAS)
    #     image_array = np.asarray(image)
    #     normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    #     data[0] = normalized_image_array
    #     predictions = model.predict(data)
    #     prediction = np.argmax(predictions, axis=-1)
    #     materials = await materials_usecases.list_materials(enabled=True)
    #     return materials[prediction[0]]

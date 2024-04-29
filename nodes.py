from PIL import Image
import torch
import numpy as np
import io

from .core import generate_watermark
import os

class InvisibleWatermarkEncode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "watermark": ("STRING", {
                    "multiline": False,
                    "default": "Hello World!"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True, )

    FUNCTION = "encode"

    CATEGORY = "WATERMARK"

    def encode(self, images, watermark):
        results = []
        for image in images:
            i = 255. * image.cpu().numpy()
            image_pil = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            image_np_array = np.array(image_pil)

            current_file_path = os.path.abspath(__file__)
            font_path = os.path.join(os.path.dirname(current_file_path), "font/ZiTiQuanWeiJunHei-W1-2.ttf")
            result_image_pil = generate_watermark(
                image_np_array, watermark, 
                font=font_path
            )

            result_image_pil = result_image_pil.convert("RGB")
            result_image_np = np.array(result_image_pil).astype(np.float32) / 255.0
            result_image_tensor = torch.from_numpy(result_image_np)[None,]
            results.append(result_image_tensor)

        return (results, )


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "InvisibleWatermarkEncode": InvisibleWatermarkEncode,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "InvisibleWatermarkEncode": "Invisible Watermark Encode",
}

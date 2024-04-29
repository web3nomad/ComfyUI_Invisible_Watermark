import base64
from PIL import Image
import torch
import numpy as np
import io

from .core import generate_watermark

class InvisibleWatermarkEncode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "encode"

    OUTPUT_NODE = True

    CATEGORY = "WATERMARK"

    def encode(self, images: list[torch.Tensor]):
        results = []
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            result_img = generate_watermark(img, "Hello, World!")
            results.append(result_img)
        return {"ui": {"images": results}}


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "InvisibleWatermarkEncode": InvisibleWatermarkEncode,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "InvisibleWatermarkEncode": "Invisible Watermark Encode",
}

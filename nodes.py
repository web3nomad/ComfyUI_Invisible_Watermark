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
                "extension": (['png', 'jpeg', 'webp'],),
                "watermark": ("STRING", {
                    "multiline": False,
                    "default": "Hello World!"
                }),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "encode"

    OUTPUT_NODE = True

    CATEGORY = "WATERMARK"

    def encode(self, images: list[torch.Tensor], extension: str, watermark: str):
        results = []
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img_i = np.array(img)
            img_o = generate_watermark(img_i, watermark)
            buffered = io.BytesIO()
            img_o.save(buffered, optimize=False, format=extension, compress_level=4)
            base64_image = base64.b64encode(buffered.getvalue()).decode()
            results.append(base64_image)
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

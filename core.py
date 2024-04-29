from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math

# Constants
DEFAULT_ASPECT_RATIO = 0.6
FONT_COLOR = (0, 0, 0)
MARGIN = 1.1


def get_text_square(txt, font_h, aspect_r=DEFAULT_ASPECT_RATIO):
    if not txt:
        return {
            'lineArr': [],
            'numLines': 0,
            'width': 10,
            'height': 10
        }

    max_line_len = math.ceil(math.sqrt(len(txt)) * 2)
    word_arr = txt.split(' ')
    line_arr = []

    while word_arr:
        line = ""
        while word_arr and len(line_arr) < max_line_len:
            line += word_arr.pop(0) + ' '
        line_arr.append(line.strip())

    actual_max_line_len = max(len(s) * 2 for s in line_arr)
    return {
        'lineArr': line_arr,
        'numLines': len(line_arr),
        'width': math.ceil(font_h * aspect_r * actual_max_line_len),
        'height': font_h * len(line_arr)
    }


def write_on_txt_canvas(width, height, txt_to_embed, font_h, margin=MARGIN, font=None):
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    _font_h = int(height * font_h)
    _font = ImageFont.truetype(font, _font_h) if font else None
    text_square = get_text_square(txt_to_embed, _font_h)
    x_offset = 5
    y_offset = 5

    width_factor = text_square['width'] * margin
    height_factor = text_square['height'] * margin

    for i in range(int(height / height_factor)):
        for j in range(int(width / width_factor)):
            for k in range(text_square['numLines']):
                x_pos = x_offset + j * width_factor
                y_pos = y_offset + i * height_factor + (k + 1) * _font_h
                draw.text((x_pos, y_pos), text_square['lineArr'][k], fill=FONT_COLOR, font=_font)

    return np.uint8(img)


def add_watermark(processing_data, txt_data):
    mask = txt_data[:, :, 3] != 0

    # 显式将数据类型更改为 uint8
    processing_data = processing_data.astype(np.uint8)

    # 进行位操作
    processing_data[mask, :3] = processing_data[mask, :3] & ~1
    processing_data[~mask, :3] = processing_data[~mask, :3] | 1
    return processing_data


def generate_watermark(input_image, wm_txt, font=None, font_h=0.025):
    text_image = write_on_txt_canvas(input_image.shape[1],
                                     input_image.shape[0], txt_to_embed=wm_txt,
                                     font_h=font_h,
                                     font=font)
    result_img_data = add_watermark(input_image, text_image)
    result_img = Image.fromarray(result_img_data)
    return result_img

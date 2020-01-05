#coding=utf-8
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np
import cv2
import codecs
import random

def resize_with_pad(image, new_size, pad_val = 255):
    resize_width, resize_height = new_size
    height, width = image.shape[0], image.shape[1]
    scale = min(float(resize_height) / height, float(resize_width) / width)
    new_height, new_width = int(height * scale), int(width * scale)
    image = cv2.resize(image, (new_width, new_height))

    pad_l = (resize_width - new_width) // 2
    pad_t = (resize_height - new_height) // 2

    res_shape = list(image.shape)
    res_shape[0], res_shape[1] = resize_height, resize_width
    res_image = np.zeros(res_shape, dtype=np.uint8) + pad_val
    res_image[pad_t:pad_t+new_height, pad_l:pad_l+new_width] = image

    return res_image

def rand_crop(image, max_width_rate, max_height_rate):
    height, width = image.shape[0], image.shape[1]
    crop_height = int(random.uniform(max_height_rate, 1.0) * height)
    crop_width = int(random.uniform(max_width_rate, 1.0)*width)

    y = 0 if crop_height == height else random.randint(0, height - crop_height)
    x = 0 if crop_width == width else random.randint(0, width - crop_width)
    crop_image = image[y:y+crop_height,x:x+crop_width]
    return crop_image

def get_image_paths(image_dir, post_fixes = ['.jpg', '.png', '.jpeg', '.bmp', '.webp', '.tif']):
    img_paths = []
    for filename in os.listdir(image_dir):
        filepath = os.path.join(image_dir, filename)
        for post_fix in post_fixes:
            if filepath.lower().endswith(post_fix):
                img_paths.append(filepath)
        if os.path.isdir(filepath):
            img_paths.extend(get_image_paths(filepath, post_fixes))
    return img_paths

def draw_text(font, image, pos, word, fill):
    pil_image = Image.fromarray(image.astype('uint8')).convert('RGB')
    draw = ImageDraw.Draw(pil_image)
    draw.text(pos, word, font=font, fill=fill)
    return np.array(pil_image, dtype=np.uint8)

def draw_outline_text(font, image, pos, word, fill, outlinefill, offset):
    pil_image = Image.fromarray(image.astype('uint8')).convert('RGB')
    draw = ImageDraw.Draw(pil_image)
    x, y = pos
    draw.text((x-offset, y), word, font=font, fill=outlinefill)
    draw.text((x, y-offset), word, font=font, fill=outlinefill)
    draw.text((x+offset, y), word, font=font, fill=outlinefill)
    draw.text((x, y+offset), word, font=font, fill=outlinefill)

    draw.text((x-offset, y-offset), word, font=font, fill=outlinefill)
    draw.text((x-offset, y+offset), word, font=font, fill=outlinefill)
    draw.text((x+offset, y+offset), word, font=font, fill=outlinefill)
    draw.text((x+offset, y-offset), word, font=font, fill=outlinefill)

    draw.text(pos, word, font=font, fill=fill)
    return np.array(pil_image, dtype=np.uint8)

def get_word_box(font, word):
    fontsize = font.size
    image = Image.new('L', (fontsize * 2, fontsize* 3), 0)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), word, font=font, fill=(255))
    array = np.array(image, dtype=np.uint8)
    row_sum = np.sum(array, axis=0)
    col_sum = np.sum(array, axis=1)
    x1 = 0
    x2 = len(row_sum)
    y1 = 0
    y2 = len(col_sum)
    for x in range(0, len(row_sum)):
        if row_sum[x] > 0:
            x1 = x
            break
    for x in range(0, len(row_sum)):
        if row_sum[len(row_sum) - 1 - x] > 0:
            x2 = len(row_sum) - x
            break 
    for y in range(0, len(col_sum)):
        if col_sum[y] > 0:
            y1 = y
            break
    for y in range(0, len(col_sum)):
        if col_sum[len(col_sum) - 1 - y] > 0:
            y2 = len(col_sum) - y
            break
    return (x1, y1, x2, y2)

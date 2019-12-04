import numpy
import cv2
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

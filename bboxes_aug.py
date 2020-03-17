#coding=utf-8
import os
import numpy as np
import cv2
from random import randint

a = 'fruit-detection/JPEGImages/banana_26.jpg 129,57,636,348,49'
a = 'fruit-detection/JPEGImages/apple_10.jpg 117,164,1423,1397,30'
#a = 'fruit-detection/JPEGImages/apple_11.jpg 213,33,442,244,30 1,30,188,280,30 141,1,337,220,30'
b = 'fruit-detection/JPEGImages/apple_1.jpg 25,56,308,341,30'

def read_lines(filepath):
    lines = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            lines.append(line)

    return lines

def parse_label_line(label_line):
    line = label_line.split()
    image_path = line[0]
    if not os.path.exists(image_path):
        raise KeyError("%s does not exist ... " %image_path)
    image = np.array(cv2.imread(image_path))
    bboxes = np.array([list(map(lambda x: int(float(x)), box.split(','))) for box in line[1:]])
    #bboxes = [list(map(lambda x: int(float(x)), box.split(','))) for box in line[1:]]
    return image, bboxes

def pad_to_square(image):
    h, w = image.shape[:2]
    if h == w:
        return image
    if h < w:
        pad_b = w - h
        image = cv2.copyMakeBorder(image, 0, pad_b, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    else:
        pad_r = h - w
        image = cv2.copyMakeBorder(image, 0, 0, 0, pad_r, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    return image

def rand_crop(image, bboxes):
    h, w = image.shape[:2]
    xmin = int(np.min(bboxes[:, 0:4:2]))
    xmax = int(np.max(bboxes[:, 0:4:2]))
    ymin = int(np.min(bboxes[:, 1:4:2]))
    ymax = int(np.max(bboxes[:, 1:4:2]))
    xmin_crop = randint(0, xmin) if xmin > 0 else 0
    xmax_crop = randint(xmax, w) if xmax < w else w
    ymin_crop = randint(0, ymin) if ymin > 0 else 0
    ymax_crop = randint(ymax, h) if ymax < h else h
    image = image[ymin_crop:ymax_crop, xmin_crop:xmax_crop]
    bboxes[:, 0:4:2] = bboxes[:, 0:4:2] - xmin_crop
    bboxes[:, 1:4:2] = bboxes[:, 1:4:2] - ymin_crop
    return image, bboxes


def resize_square(image, bboxes, target_size):
    h, w = image.shape[:2]
    if h != w:
        print('not square image')
        return image, bboxes

    if h == target_size:
        return image, bboxes

    scale = float(target_size) / h
    image = cv2.resize(image, (target_size, target_size))
    bboxes[:,:4] = bboxes[:,:4] * scale
    return image, bboxes

def merge(image, bboxes, image_yat, bboxes_yat):
    h, w = image.shape[:2]
    if h != w:
        print('not square')
        return images, bboxes

    if image.shape != image_yat.shape:
        print('shape mismatch')
        return image, bboxes


    if randint(0, 1):
        w_shift = randint(0, w)
        bboxes[:,0:4:2] = bboxes[:,0:4:2] + w_shift
        image_large = cv2.copyMakeBorder(image, 0, h, w_shift, w - w_shift, cv2.BORDER_CONSTANT, value=(255, 255, 255)) 
        cv2.imwrite('larger.jpg', image_large)
        x = randint(0, w)
        y = h
    else:
        h_shift = randint(0, h)
        bboxes[:,1:4:2] = bboxes[:,1:4:2] + h_shift
        image_large = cv2.copyMakeBorder(image, h_shift, h - h_shift, 0, w, cv2.BORDER_CONSTANT, value=(255, 255, 255)) 
        cv2.imwrite('larger.jpg', image_large)
        x = w
        y = randint(0, h)

    image_large[y:y+h, x:x+w] = image_yat
    bboxes_yat[:,0:4:2] = bboxes_yat[:,0:4:2] + x
    bboxes_yat[:,1:4:2] = bboxes_yat[:,1:4:2] + y
    bboxes = np.concatenate((bboxes, bboxes_yat), axis=0)
    return image_large, bboxes

def check_bboxes(image, bboxes):
    h, w = image.shape[:2]
    xmin = int(np.min(bboxes[:, 0:4:2]))
    xmax = int(np.max(bboxes[:, 0:4:2]))
    ymin = int(np.min(bboxes[:, 1:4:2]))
    ymax = int(np.max(bboxes[:, 1:4:2]))
    bbox_w = xmax - xmin
    bbox_h = ymax - ymin

    if bbox_w > 0.9 * w and bbox_h > 0.9 * h:
        return False
    if bbox_w < 0.4 * w and bbox_h < 0.4 * h:
        return False

    for i in range(len(bboxes)):
        bbox = bboxes[i]
        xmin, ymin, xmax, ymax = bbox[:4]
        bbox_w = xmax - xmin
        bbox_h = ymax - ymin
        if bbox_w > 0.9 * w and bbox_h > 0.9 * h:
            return False
        if bbox_w < 0.4 * w and bbox_h < 0.4 * h:
            return False

        if bbox_w < 0.3 * w or bbox_h < 0.3 * h:
            return False
    
    return True

def try_to_merge(line, line_yat):
    image, bboxes = parse_label_line(line)
    if not check_bboxes(image, bboxes):
        return image, bboxes
    image_yat, bboxes_yat = parse_label_line(line_yat)
    if not check_bboxes(image_yat, bboxes_yat):
        return image, bboxes

    image, bboxes = rand_crop(image, bboxes)
    image = pad_to_square(image)
    image_yat, bboxes_yat = rand_crop(image_yat, bboxes_yat)
    image_yat = pad_to_square(image_yat)

    target_size = max(image.shape[0], image_yat.shape[0])
    image, bboxes = resize_square(image, bboxes, target_size)
    image_yat, bboxes_yat = resize_square(image_yat, bboxes_yat, target_size)
    cv2.imwrite('resize_yat.jpg', image_yat)

    image, bboxes = merge(image, bboxes, image_yat, bboxes_yat)

    xmin = int(np.min(bboxes[:, 0:4:2]))
    xmax = int(np.max(bboxes[:, 0:4:2]))
    ymin = int(np.min(bboxes[:, 1:4:2]))
    ymax = int(np.max(bboxes[:, 1:4:2]))
    image = pad_to_square(image)
    image_yat, bboxes_yat = parse_label_line(line)
    image_yat = pad_to_square(image_yat)

    return image, bboxes





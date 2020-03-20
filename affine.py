import cv2
from math import *
import numpy as np

def rotate_image(image, angle, target_size=None, crop=True):
    height, width = image.shape[:2]
    rotation_mat = cv2.getRotationMatrix2D((width/2.,height/2.),angle,1)
    if target_size:
        new_width, new_height = target_size
    elif crop:
        new_height = height
        new_width = width
    else:
        new_height =int(width*fabs(sin(radians(angle)))+height*fabs(cos(radians(angle))))
        new_width =int(height*fabs(sin(radians(angle)))+width*fabs(cos(radians(angle))))

    rotation_mat[0,2] +=(new_width - width)/2 #重点在这步，目前不懂为什么加这步
    rotation_mat[1,2] +=(new_height - height)/2 #重点在这步

    rotated_image = cv2.warpAffine(image, rotation_mat, (new_width, new_height),borderValue=(255,255,255))
    return rotated_image, rotation_mat
    
def get_target_pts(mat, pts):
    pts = np.dot(mat, list(pts) + [1])
    x, y = int(pts[0]), int(pts[1])
    return [x, y]

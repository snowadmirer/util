#coding=utf-8
import lxml
import cv2

def read_voc_label(label_file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(label_file, parser)
    size = tree.find('size')
    height = int(size.find('height').text)
    width = int(size.find('width').text)
    
    labels = []
    for object in tree.findall('object'):
        bndbox = object.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        name = object.find('name').text
        labels.append((xmin, ymin, xmax, ymax, name))

    return labels

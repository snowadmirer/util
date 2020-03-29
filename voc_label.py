#coding=utf-8
from lxml import etree, objectify
import cv2
import os

def read_voc_label(label_file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(label_file, parser)
    size = tree.find('size')
    height = int(size.find('height').text)
    width = int(size.find('width').text)
    
    labels = []
    for object in tree.findall('object'):
        bndbox = object.find('bndbox')
        xmin = int(float(bndbox.find('xmin').text))
        ymin = int(float(bndbox.find('ymin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymax = int(float(bndbox.find('ymax').text))
        name = object.find('name').text
        labels.append((xmin, ymin, xmax, ymax, name))

    return labels

def make_voc_label(filepath, height, width, bboxes, savepath):
    filename = os.path.basename(filepath)
    folder = os.path.dirname(filepath.replace('/apsarapangu/disk2/jiade.pjd/data/ingredient/classify_label', ''))
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
                E.folder(folder),
                E.filename(filename),
                E.size(
                    E.width(width),
                    E.height(height),
                    E.depth(3)
                ),

                )
    for bbox in bboxes:
        xmin, ymin, xmax, ymax = bbox[:4]
        class_name = bbox[4]
        obj = E.object(
            E.name(class_name),
            E.pose('Unspecified'),
            E.difficult('0'),
            E.bndbox(
                E.xmin(str(xmin)),
                E.ymin(str(ymin)),
                E.xmax(str(xmax)),
                E.ymax(str(ymax)),
            ),
        )
        anno_tree.append(obj)

    etree.ElementTree(anno_tree).write(savepath, pretty_print=True)

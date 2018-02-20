import cv2
import json
from keras import backend as K
from keras.models import load_model
# from vgg16 import VGG16
import argparse
import numpy as np
import os
import random
import sys

def _load_model(weights):
    model = load_model(weights)
    return model

def load_classes(file):
    with open(file, 'r') as class_file:
        json_data = class_file.read()
    return json.loads(json_data)


def predict(model, image):
    
    image = cv2.resize(image,(256,256))
    image = np.array(image)
    image = image.astype('float32')
    image /= 255        
    image= np.expand_dims(image, axis=0)

    preds = model.predict_classes(image)[0]
    return preds #names[preds]

def load_placement_from_json(json_file):
    with open(json_file, 'r') as json_file:
        data = json.loads(json_file.read())

    return data


# res = {}
def pred(im_file):
    
    model = _load_model('../custom_cnn/models/weights-cigarettes-107-015-0.3907-0.8931--0.9789.h5')
    classes = load_classes('../custom_cnn/category.json')

    im_arr = np.load(im_file)
    # for i in load[()].keys():
    #     cv2.imshow('crop', load[()][i])
    #     cv2.waitKey(0)
    placement = {'Shelf1': {}}
    for i in im_arr[()].keys():
        im = im_arr[()][i]
        pred = predict(model, im)
        # print(i, pred, classes[pred])
        # crop = cv2.resize(crop,(256,256))
        # cv2.imshow('pred', im)
        # cv2.putText(crop, "Label: {}".format(pred), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        # cv2.waitKey(0)

        placement['Shelf1'][i+1] = classes[pred]
        # cv2.imshow('crop', crop)
        # cv2.waitKey(0)
        # package_id += 1
    # print(placement)
    with open('placement.json', 'w') as json_file:
        json.dump(placement, json_file)
    return placement


if __name__ == "__main__":

    pred('temp.npy')
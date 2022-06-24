import sys
import os
from PIL import Image
import shutil
import random
import glob
import matplotlib.pyplot as plt
import numpy as np

## 라벨링 한 이미지가 254 등 잡다한 값이 있을 경우 변환 하는 코드
dir_train = './veindata/train/'\

label_list = glob.glob(dir_train+'label*')

LABEL_TO_COLOR = {0:[0,0,0], 1:[255,0,0], 2:[0,255,0], 3:[0,0,255]}

def mask2rgb(mask):
    
    rgb = np.zeros(mask.shape+(3,), dtype=np.uint8)
    
    for i in np.unique(mask):
            rgb[mask==i] = LABEL_TO_COLOR[i]
            
    return rgb

def rgb2mask(rgb):
    
    mask = np.zeros((rgb.shape[0], rgb.shape[1]))

    for k,v in LABEL_TO_COLOR.items():
        mask[np.all(rgb==v, axis=2)] = k
        
    return mask

for i in range(0,105):
    img_dir = label_list[i]
    
    img = Image.open(img_dir).convert("L")
    img = np.array(img)
    img = img/255
    img = np.floor(img)
    img = -(img-1)
    print(img.shape)
    
    img = mask2rgb(img)
    img = Image.fromarray(img)
    img.save(img_dir)
    img = np.array(img)
    print(np.min(img[np.nonzero(img)]))



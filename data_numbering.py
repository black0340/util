import sys
import os
from PIL import Image
import shutil
import random

## 이미지 분류 하는 코드 num부터 시작 nframe_ 으로 비율 변환
dir_data = '.././origindata/rat_real/06-24-rearat_injectiontest/top/img2'

dir_save_train = os.path.join(dir_data,'train')
dir_save_val = os.path.join(dir_data, 'val')
dir_save_test = os.path.join(dir_data,'test')

resizing= False        #resize 여부 체크
lastnum = 805

resize_witdh = 2048
resize_height = 2048
# NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS
resize_filter = Image.LANCZOS
resize_var = (resize_witdh,resize_height)

if not os.path.exists(dir_save_train):
    os.makedirs(dir_save_train)
if not os.path.exists(dir_save_val):
    os.makedirs(dir_save_val)
if not os.path.exists(dir_save_test):
    os.makedirs(dir_save_test)

nframe_train = 1
nframe_val = 0
nframe_test = 0

image_list = [f for f in os.listdir(dir_data) if os.path.isfile(f'{dir_data}/{f}')]
random.shuffle(image_list)
num_image = len(image_list)
print(f'image number = {num_image}')
nframe_train_num = int(num_image*nframe_train)+1
nframe_val_num = int(num_image*nframe_val)
nframe_test_num = num_image-nframe_train_num-nframe_val_num
sum_image = nframe_train_num+nframe_test_num+nframe_val_num

if sum_image != num_image:
    print(f"image number of err check the nframe// sum = {sum_image}, real {num_image}")
    sys.exit()

for i in range(0,num_image):
    if i==0 or nframe_train_num==i or nframe_train_num+nframe_val_num==i:
        j=0
    img = Image.open(f'{dir_data}/{image_list[i]}')
    if resizing == True:
        img = img.resize(resize_var,resize_filter)

        if i<nframe_train_num:
            print(f'this : {dir_data}/{image_list[i]}, to : {dir_save_train}/input_{j+lastnum:0>3}.png')
            img.save(f'{dir_save_train}/input_{j+lastnum:0>3}.png')
            # shutil.copy(f'{dir_data}/{image_list[i]}', f'{dir_save_train}/input_{j:0>3}.png')
        elif i <nframe_train_num+nframe_val_num:
            print(f'this : {dir_data}/{image_list[i]}, to : {dir_save_val}/input_{j+lastnum:0>3}.png')
            img.save(f'{dir_save_val}/input_{j+lastnum:0>3}.png')
            # shutil.copy(f'{dir_data}/{image_list[i]}', f'{dir_save_val}/input_{j:0>3}.png')
        else:
            print(f'this : {dir_data}/{image_list[i]}, to : {dir_save_test}/input_{j+lastnum:0>3}.png')
            img.save(f'{dir_save_test}/input_{j+lastnum:0>3}.png')
            # shutil.copy(f'{dir_data}/{image_list[i]}', f'{dir_save_test}/input_{j:0>3}.png')
    else:
        if i<nframe_train_num:
            print(f'this : {dir_data}/{image_list[i]}, to : {dir_save_train}/input_{j+lastnum:0>3}.png')
            shutil.copy(f'{dir_data}/{image_list[i]}', f'{dir_save_train}/input_{j:0>3}.png')
        elif i <nframe_train_num+nframe_val_num:
            print(f'this : {dir_data}/{image_list[i]}, to : {dir_save_val}/input_{j+lastnum:0>3}.png')
            shutil.copy(f'{dir_data}/{image_list[i]}', f'{dir_save_val}/input_{j:0>3}.png')
        else:
            print(f'this : {dir_data}/{image_list[i]}, to : {dir_save_test}/input_{j+lastnum:0>3}.png')
            shutil.copy(f'{dir_data}/{image_list[i]}', f'{dir_save_test}/input_{j:0>3}.png')

    j= j+1

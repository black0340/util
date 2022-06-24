
import os
from PIL import Image
import cv2
import re

## 이미지 분류 하는 코드 num부터 시작 nframe_ 으로 비율 변환
dir_data = '.././origindata/05_30-realrat_pme2\color_images'


t_data = dir_data+'/train'
v_data = dir_data+'/val'

t_data_save = os.path.join(dir_data,'con_train')
v_data_save = os.path.join(dir_data,'con_val')

resizing= False        #resize 여부 체크

resize_witdh = 2048
resize_height = 2048
# NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS
resize_filter = Image.LANCZOS
resize_var = (resize_witdh,resize_height)

if not os.path.exists(t_data_save):
    os.makedirs(t_data_save)
if not os.path.exists(v_data_save):
    os.makedirs(v_data_save)


t_image_list = [f for f in os.listdir(t_data) if os.path.isfile(f'{t_data}/{f}')]
t_image_list_input = [file for file in t_image_list if file.startswith("input")]
t_num_image = len(t_image_list_input)

print(f"image number = {t_num_image}")

for i in range(0,t_num_image):
    i_num = re.sub(r'[^0-9]','',t_image_list_input[i])
    img = cv2.imread(f'{t_data}/{t_image_list_input[i]}',cv2.IMREAD_COLOR)
    lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)

    # l, a, b 채널 분리
    l, a, b = cv2.split(lab)

    # CLAHE 객체 생성
    clahe = cv2.createCLAHE(clipLimit=4.0,tileGridSize=(8, 8))
    # CLAHE 객체에 l 채널 입력하여 CLAHE가 적용된 l 채널 생성 
    l = clahe.apply(l)

    # l, a, b 채널 병합
    lab = cv2.merge((l, a, b))
    # lab 색공간 이미지를 bgr 색공간 이미지로 변환
    cont_dst = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    cv2.imwrite(f"{t_data_save}/cnt_{i_num}.png",cont_dst)


v_image_list = [f for f in os.listdir(v_data) if os.path.isfile(f'{v_data}/{f}')]
v_image_lisv_input = [file for file in v_image_list if file.startswith("input")]
v_num_image = len(v_image_lisv_input)

for i in range(0,v_num_image):
    i_num = re.sub(r'[^0-9]','',v_image_lisv_input[i])
    img = cv2.imread(f'{v_data}/{v_image_lisv_input[i]}',cv2.IMREAD_COLOR)
    lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)

    # l, a, b 채널 분리
    l, a, b = cv2.split(lab)

    # CLAHE 객체 생성
    clahe = cv2.createCLAHE(clipLimit=4.0,tileGridSize=(8, 8))
    # CLAHE 객체에 l 채널 입력하여 CLAHE가 적용된 l 채널 생성 
    l = clahe.apply(l)

    # l, a, b 채널 병합
    lab = cv2.merge((l, a, b))
    # lab 색공간 이미지를 bgr 색공간 이미지로 변환
    conv_dst = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    cv2.imwrite(f"{v_data_save}/cnt_{i_num}.png",cont_dst)
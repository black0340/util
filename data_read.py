import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

## 튜토리얼 dataread
dir_data = './data'

name_label = 'train-labels.tif'
name_input = 'train-volume.tif'

image_label = Image.open(os.path.join(dir_data, name_label))
image_input = Image.open(os.path.join(dir_data, name_input))

ny, nx =  image_label.size
nframe = image_label.n_frames


nframe_train =24
nframe_val = 3
nframe_test = 3

dir_save_train = os.path.join(dir_data,'train')
dir_save_val = os.path.join(dir_data, 'val')
dir_save_test = os.path.join(dir_data,'test')

if not os.path.exists(dir_save_train):
    os.makedirs(dir_save_train)
if not os.path.exists(dir_save_val):
    os.makedirs(dir_save_val)
if not os.path.exists(dir_save_test):
    os.makedirs(dir_save_test)


id_frame = np.arange(nframe)
print(f'id_frame = {id_frame}')
np.random.shuffle(id_frame)

offset_nframe = 0

# a = f'{5:0>3}'
# print(a)  #005
for i in range(nframe_train):
    image_label.seek(id_frame[i+offset_nframe])
    image_input.seek(id_frame[i+offset_nframe])
    

    label_ = np.asarray(image_label)
    input_ = np.asarray(image_input)

    np.save(os.path.join(dir_save_train,f'label_{i:0>3}.npy'),label_)
    np.save(os.path.join(dir_save_train,f'input_{i:0>3}.npy'),input_)

offset_nframe += nframe_train
for i in range(nframe_val):
    image_label.seek(id_frame[i+offset_nframe])
    image_input.seek(id_frame[i+offset_nframe])

    label_ = np.asarray(image_label)
    input_ = np.asarray(image_input)

    np.save(os.path.join(dir_save_val,f'label_{i:0>3}.npy'),label_)
    np.save(os.path.join(dir_save_val,f'input_{i:0>3}.npy'),input_)

offset_nframe += nframe_test
for i in range(nframe_val):
    image_label.seek(id_frame[i+offset_nframe])
    image_input.seek(id_frame[i+offset_nframe])

    label_ = np.asarray(image_label)
    input_ = np.asarray(image_input)

    np.save(os.path.join(dir_save_test,f'label_{i:0>3}.npy'),label_)
    np.save(os.path.join(dir_save_test,f'input_{i:0>3}.npy'),input_)


plt.subplot(121)
plt.imshow(label_, cmap='gray')
plt.title('label')

plt.subplot(122)
plt.imshow(input_, cmap='gray')
plt.title('intput')

plt.show()
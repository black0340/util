import cv2 
from glob import glob
import os
import timeit
# count = 0
# for i in range(1,7):

#     vidcap = cv2.VideoCapture(f'./{i}.mp4')
    
#     while(vidcap.isOpened()): 
#         ret, image = vidcap.read() 
#         if not ret:
#             break
#         if(int(vidcap.get(1)) % 30 == 0): 
#             print('Saved frame number : ' + str(int(vidcap.get(1)))) 
#             cv2.imwrite("./img/mouse_%d.jpg" % count, image) 
#             print('Saved frame%d.jpg' % count) 
#             count += 1 
        

# vidcap.release()

date = "06-24"
file_name = ("MOV","mp4")
cut_frame = 240
img_dir = './img2'
if not os.path.exists(img_dir):
        os.makedirs(img_dir)


files = [fn for fn in glob('*') if os.path.basename(fn).endswith(file_name)]
count = 0
for file in files:
    vidcap = cv2.VideoCapture(f'{file}')
    i = 0
    while(vidcap.isOpened()):
        grab = vidcap.grab()
        if i % cut_frame == 0:
            ret, image = vidcap.retrieve()
            if not ret:
                break
            print('Saved frame number : ' + str(int(i))) 
            cv2.imwrite(f"{img_dir}/img_{count}.jpg", image) 
            print(f'Saved img_{count}.jpg') 
            count += 1
        i+=1
        
        #if(int(vidcap.get(1)) % cut_frame == 0):   
        
vidcap.release()
from glob import glob
import cv2
import os



# file_name으로 끝나는 파일들 찾아서 files에 list로 저장
# fn에 glob으로 모든파일 불러오는데 만약 파일네임이 file_name으로 끝나는 경우
file_name = ("tif")
files = [fn for fn in glob('*') if fn.endswith(file_name)] 
pngdir = "./png"
if not os.path.exists(pngdir):
    os.makedirs(pngdir)
for file in files:
    img = cv2.imread(f'{file}')
    cv2.imwrite(f"{pngdir}/{file}.png",img)
    print(file)

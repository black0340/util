# util
잡일

cvtlabeling.py
=> gimp로 라벨링 잘못했을 떄 threshold 같이 함 
-픽셀값이 일정해야하는데 254 같은거 껴있을때 threshold

data_numbering.py
=> 데이터셋 변환용 파일명 변경 및 train val test 분류 또는 resize
-파일 분류용


data_read.py
=> unet 튜토리얼 data_read.py 
-딥러닝 데이터 불러오기


makeblank.py
=> 검정이미지 생성
-라벨링 안된 이미지들 검정색(0) 으로 라벨링 이미지 생성

videoslice.py
=> 영상에서 프레임 추출
-원하는 프레임으로 폴더안의 영상들 전부 프레임 추출

tiftopng.py
=> tif확장자를 png파일로 변경 jpg등등 opencv로 저장가능하거나 불러오는것들 
-잘못 저장된 이미지들 호환 안될때 폴더안의 이미지들 전부 변환 

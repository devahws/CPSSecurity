import picamera         # 파이카메라 모듈 import
import time
import datetime         # 파일 이름 저장을 위해 datetime 모듈 import
import os               # 파일 경로 사용을 위해 os import
import os.path

path = os.getcwd()  # camerashot.py 파일이 존재하는 파일 경로를 설정

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)              # 카메라 해상도를 640x480으로 설정
    while True:
        new_dir_name = os.path.join(path, datetime.datetime.now().strftime('%Y-%m-d-%H:%M')) # 분 단위로 디렉토리 생성
        for i in range(10):                     # 한 번 촬영할 때 10장의 사진 촬영
            now = datetime.datetime.now()       # 사진을 촬영할 때의 시간
            filename = new_dir_name +'/'+ now.strftime('%Y-%m-d-%H:%M')     # 파일 이름생성
            camera.capture(filename+'.jpg')                                 # 사진을 촬영한 후 저장
            time.sleep(5)       # 5초에 한 장씩 촬영
        time.sleep(1750)        # 30분에 한 번씩 10장씩 촬영하도록 설정



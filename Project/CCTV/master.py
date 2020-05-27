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


def save_img(data): # 전달받은 이미지를 저장
    img_fileName = fileName()               # fileName() 함수를 통해 저장할 파일의 이름 설정
    img_file = open(img_fileName, "wb")     # 파일을 저장하기 위해 쓰기 모드로 지정한 이름의 파일 생성
    print("finish img recv")                # 서버에게 정보를 전달받았다는 안내 문구
    print(sys.getsizeof(data))              # 인자로 전달받은 data의 크기를 출력
    img_file.write(data)                    # wb모드로 생성한 img_file에 전달받은 data를 입력
    img_file.close()                        # img_file 스트림을 close
    print("Finish ")                        # 파일 저장을 나타내는 안내 문구 출력

def receive_img():  # 클라이언트에게 이미지를 전달받는 프로그램
    img_data = client_socket.recv(1024)     # 연결된 클라이언트 소켓에게 데이터를 recv
    data = img_data                         # 변수 데이터에 전달받은 img_data를 저장
    if img_data:                            # 전달받은 data가 존재한다면 실행
        while img_data:                     # 전달받은 data를 모두 옮기기 전까지 실행
            print("****************************recving Img...****************************")
            img_data = client_socket.recv(60000)  # 제일 큰 사진 용량에 따라 설정
            data += img_data
            save_img(data)                        # save_img 함수에 클라이언트에게 전송받은 data를 인자로 전달
            if img_data[-9:] == 'finish':         # 서버로부터 파일 전송 마무리를 알리는 'finish'를 전달받으면 프로그램 종료
                break

def run_master(client_socket):               # master.py 프로그램을 실행하는 함수
    while True:                     # 1시간마다 실행하기 위해 무한 반복
        client_socket.send('get'.encode())              # 서버에게 데이터 전송을 요청하기 위해 'get 데이터 전송
        file_count = client_socket.recv(1024).decode()  # 서버로부터 서브 디렉토리의 개수 수신
        file_count = json.loads(file_count)              # json 자료형 데이터를 loads하여 저장
        size = file_count.get("size")   # for문에서 사용할 서브 디렉토리 개수 저장
        for i in range(size):           # 전달받은 서브 디렉토리의 길이만큼 for문 실행
            receive_img()               # 이미지를 전송 받아서 저장
        time.sleep(3600)                # 1시간에 한 번씩 데이터를 전송받도록 설계

if __name__ == '__main__':
    # 클라이언트 소켓을 생성하며 지정된 IP와 포트의 서버주소와 연결
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.0.11", 4444))
    # 서버로부터 전송받은 데이터를 저장하는 run_master 함수 실행
    run_master(client_socket)


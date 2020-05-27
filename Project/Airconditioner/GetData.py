# GetData.py
# 클라이언트에게 전달받은 날씨 정보와 미세먼지 정보를 처리하는 프로그램

from socket import *            # 서로 다른 호스트에 존재하는 기기끼리 통신하기 위해 Socket API import
import json                     # TCP 통신에서 데이터를 담을 컨테이너로 json 사용
import sys                      # 예외처리 상황에서 프로그램을 종료시키기 위해 sys import
import time                     # 타이머 기능을 사용하기 위해 time import

try:
    serverPort = 5555                               # 서버 프로그램에서 사용할 포트를 지정
    serverSocket = socket(AF_INET, SOCK_STREAM)     # TCP 프로토콜을 사용하는 서버 소켓 생성
    serverSocket.bind(('', serverPort))             # 프로그램이 존재하는 IP주소의 포트에 소켓 연결
    serverSocket.listen(1)                          # 클라이언트의 연결을 기다리는 상태
    print("The server is ready to receive on port", serverPort) # 서버가 작동하고 있음을 나타내는 안내문구

    (connectionSocket, clientAddress) = serverSocket.accept()   # 연결된 클라이언트 소켓의 정보를 저장
except KeyboardInterrupt:       # ctlr+c 키를 통하여 프로그램 종료
    print('\nTerminate Server') # 종료 안내 문구
    serverSocket.close()        # 서버 소켓 close
    sys.exit()                  # 시스템 종료

try:    # 예외처리를 위해 try-catch 사용
    while True: # ctrl+c 키를 누르기 전까지 프로그램 무한반복
        message = connectionSocket.recv(2048)         # 클라이언트 소켓에게 받은 데이터 전달
        message = json.loads(message.decode())        # json타입에 저장된 데이터를 decode하여 저장

        if message.get("option") == 0:                # 온도와 미세먼지 정보를 나타내는 0번 옵션일 때에만 실행
            print('Get Info From Client')             # 데이터 수신 안내 문구
            tmps = message.get("temp")                # 전달받은 데이터에서 온도 데이터 저장
            matter = message.get("matter")            # 전달받은 데이터에서 미세먼지 데이터 저장

            # 온도와 미세먼지 출력
            print('현재 온도: '+str(tmps[0]))
            for i in range(1,4):
                print(str(i)+'시간 뒤 온도: '+str(tmps[i]))
            print('현재 초미세먼지 농도: '+str(matter["fpmatter"]))
            print('현재 미세먼지 농도: ' + str(matter["pmatter"]))

        # 한 시간 뒤 다시 데이터를 수신
        time.sleep(3600)

except KeyboardInterrupt:       # 사용자가 ctrl+c 키를 눌렀을 때 종료
    print('\nTerminate Server') # 종료 안내 문구
    connectionSocket.close()    # 연결된 소켓 close
    serverSocket.close()        # 서버 소켓 close
    sys.exit()                  # 시스템 종료

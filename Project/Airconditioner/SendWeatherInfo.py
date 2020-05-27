# SendWeatherInfo.py
# 1. 웹 크롤링을 통해 온도 정보와 미세먼지 정보를 수집한 뒤
# 2. 소켓 API를 활용하여 IoT 에어컨에게 수집한 정보를 전달하는 프로그램

from selenium import webdriver  # 웹 크롤링 사용을 위해 셀레니움 import
from bs4 import BeautifulSoup   # 웹 크롤링 사용을 위해 BeautifulSoup import
import os              # 파일 경로 사용을 위해 os import
from socket import *   # 서로 다른 호스트에 존재하는 기기끼리 통신하기 위해 Socket API import
import time            # 타이머 기능을 사용하기 위해 time import
import json            # TCP 통신에서 데이터를 담을 컨테이너로 json 사용
import sys             # 예외처리 상황에서 프로그램을 종료시키기 위해 sys import

serverName = "xxx.xxx.xxx.xxx"                # 통신할 서버의 IP를 설정
serverPort = 5555                             # 통신할 서버의 포트 설정

path = os.getcwd() + "/chromedriver"          # 크롬 드라이버의 path 저장
driver = webdriver.Chrome(path)               # 웹 드라이버 호출
temperature = []                              # 온도를 저장할 list
matter = {}                                   # 미세먼지를 저장할 dict

def get_Info(): # 웹 크롤링을 통해 날씨 정보와 미세먼지 정보를 가져오는 프로그램
    try:
        ## 온도 측정 ##
        driver.get("http://www.naver.com")  # Naver 날씨에서 체감 온도 정보 크롤링
        time.sleep(1)
        searchIndex = "날씨"
        element = driver.find_element_by_class_name("input_text")
        element.send_keys(searchIndex)
        driver.find_element_by_id("search_btn").click()

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        # 4시간 뒤의 체감 온도까지 저장
        tmp = bs.find_all("dd", class_="weather_item _dotWrapper")
        for i in range(5):  # 현재 날씨부터 4시간 뒤의 체감 온도 정보를 크롤링
            temperature.append(int(tmp[i].find("span").text))
        time.sleep(3)       # 프로그램 실행의 안정성을 위해 3초 sleep

        ## 미세먼지 측정 ##
        driver.get("https://cleanair.seoul.go.kr/2020/")    # 서울 미세먼지정보 홈페이지
        time.sleep(1)
        button = driver.find_element_by_xpath("//*[@id=\"map_\"]/div[1]/div[2]/div[3]/div[20]")
        button.click()  # 동작구를 나타내는 버튼을 클릭
        # 초미세먼지 정보를 저장
        fpmatter = driver.find_element_by_xpath("//*[@id=\"pm25El\"]").text
        # 미세먼지 정보를 저장
        pmatter = driver.find_element_by_xpath("//*[@id=\"pm10El\"]").text

        # 미세먼지 정보를 저장하는 matter dict에 저장
        matter["fpmatter"] = [int(fpmatter)]
        matter["pmatter"] = [int(pmatter)]
    finally:
        time.sleep(2)
        driver.quit()

def send_Info(): # 소켓 API를 사용하여 IoT 기기에게 날씨 정보를 전달하는 프로그램
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)     # TCP 프로토콜을 사용하는 클라이언트 소켓 생성
        clientSocket.connect((serverName, serverPort))  # 미리 지정한 서버의 주소와 포트에 클라이언트 소켓을 연결
    except ConnectionRefusedError:                                  # 중간에 연결이 끊겼을 때의 예외처리
        print('Server-side is not listen any request. try again')   # 안내 문구 출력
        clientSocket.close()                                        # 클라리언트 소켓 close
        sys.exit()                                                  # 프로그램 종료

    print("The client is running on port", clientSocket.getsockname()[1])  # 클라이언트가 작동하는 포트 안내
    print('Send message to IoT device')                                    # IoT 기기에게 정보를 전달한다는 안내문구
    data = json.dumps({"option": 0, "temp": temperature, "matter": matter})# json 자료형에 통해 온도 정보와 미세먼지 정보 저장
    clientSocket.send(data.encode())                                       # 연결된 서버 소켓에게 정보를 encoding하여 전달

if __name__ == '__main__':
    while True:
        get_Info()      # 정보를 수집
        send_Info()     # 정보를 전달
        print('Send data to IoT device successfully!')  # 전송을 완료했다는 안내 문구
        time.sleep(3600) # 1시간 뒤에 다시 IoT 기기에게 데이터 전송

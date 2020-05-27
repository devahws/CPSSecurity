# 페이지 로딩 시간이 인터넷 환경에 따라 차이가 있어서 그런건지 같은 코드에 같은 조건을 입력했음에도
# 결과가 정상적으로 출력될 때가 있고, 아니면 중간에 프로그램이 페이지에서 데이터를 읽어오지 못해서 그냥 종료될 때도 있습니다
# 최대한 문제를 해결해보려고 time.sleep()을 이곳저곳에 배치해놔서 프로그램 실행시간이 좀 오래 걸릴 수도 있습니다.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/chromedriver"
driver = webdriver.Chrome(path)

try:
    driver.get("https://www.airbnb.co.kr/")
    time.sleep(1)

    # 여행하려는 도시 입력
    countryIndex = input("$ 여행하려는 도시를 입력하세요 >> ")

    countryElement = driver.find_element_by_xpath("//*[@id=\"bigsearch-query-attached-query\"]")
    countryElement.send_keys(countryIndex)

    # 동일한 클래스를 가지는 날짜 버튼과 인원 버튼을 list로 만들어서 선택 사용
    button = driver.find_elements_by_class_name("_esmga25")

    # 여행 인원 입력
    button[1].click()
    time.sleep(1)
    headCount = input("$ 여행 인원을 입력하세요 >> ")
    headCountIndex = int(headCount)
    
    for i in range(headCountIndex): # 입력한 인원 수 만큼 인원 추가 버튼을 클릭
        driver.find_element_by_css_selector("#stepper-adults > button:nth-child(3)").click()

    # 원하는 조건으로 검색
    driver.find_element_by_class_name("_jpp2dbp").click()

    title = []      # 숙소의 이름
    facility = []   # 숙소의 시설
    rate = []       # 숙소의 평점
    rateCount = []  # 숙소의 후기수
    time.sleep(2)

    for i in range(5):
        time.sleep(2)
        # bs4를 통해 페이지의 주소를 가져옴
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        # bnbCard라는 변수에 숙소의 정보가 저장된 카드들을 모두 저장
        bnbCard = bs.find_all("div", class_="_tdu37o")
        # 페이지가 넘어갈 때마다 page 태그를 저장
        title.append("page: "+str(i+1))
        facility.append(" ");
        rate.append(" ");
        rateCount.append(" ");
        # 페이지에 존재하는 카드의 개수만큼 루프문을 돌면서 카드의 데이터들을 각 항목에 저장
        for c in bnbCard:
            title.append(c.find("div", class_="_1c2n35az").text)            # 숙소의 이름
            facility.append(c.find("div", class_="_kqh46o").text)           # 숙소의 시설
            rate.append(c.find("span", class_="_10fy1f8").text)             # 숙소의 평점
            rateCount.append(c.find_all("span", class_="_krjbj")[1].text)   # 숙소의 후기 수

        time.sleep(2)
        # next 버튼에서 다음 페이지로 넘어가는 href의 value를 가져와서 다음 페이지로 이동
        find = driver.find_element_by_css_selector("#ExploreLayoutController > div._e296pg > div._1gw6tte > div > div > div._1ou8uzt > nav > ul > li._i66xk8d > a")
        path1 = find.get_attribute("href")
        print("page"+ str(i+1) +" complete")
        driver.get(str(path1))
        time.sleep(1)

finally:
    # title list에 "page"가 존재할 때마다 줄바꿈 실행
    for i in range(len(title)):
        if title[i].find("page")!=-1:
            print()
            print(title[i])
        else:
            print("숙소명: "+title[i]+" // 시설: "+facility[i]+" // 평점: "+rate[i]+" //"+rateCount[i])

    time.sleep(3)

    driver.quit()

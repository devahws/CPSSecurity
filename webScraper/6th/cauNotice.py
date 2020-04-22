from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/chromedriver"

driver = webdriver.Chrome(path)

try:
    driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=2130#page1")
    time.sleep(1)   # 1초 지나고 페이지 종료
    driver.implicitly_wait(10)

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    pages = bs.find("div", class_ = "pagination").find_all("a")[-1]["href"].split("page")[1]
    pages = int(pages)

    title = []
    for i in range(3):
        driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=2130#page"+str(i+1))
        time.sleep(3)
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        cont = bs.find_all("div", class_ = "txtL")
        title.append("page" + str(i+1))
        for c in cont:
            title.append(c.find("a").text)


finally:
    for t in title:
        if t.find("page"):
            print()
            print(t)
        else:
            print(t)

    driver.quit()

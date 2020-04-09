# 교보문고 베스트셀러 컴퓨터/IT Top 100 데이터 뽑아오기

import requests
from bs4 import BeautifulSoup
import csv

class Scrapper():
    def __init__(self):
        self.url = "http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?perPage=100&mallGb=KOR&linkClass=33&menuCode=002"
        # 베스트셀러 페이지 이동이 url값 변경이 아니라 javascript: go_targetPage('2') 이런 형식으로 되어있는데
        # 어떻게 하는지 모르겠어서 그냥 베스트셀러 페이지 url에서 'perPage' 변수를 100으로 직접 변경해서 상위 100개의 책 정보를 가져옴

    def getHTML(self):
        res = requests.get(self.url)

        if res.status_code != 200:
            print("request error : ", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getCards(self, soup):
        bookCards = soup.select(".id_detailli") # bookCards로부터 제목, 평점, 저자, 가격 정보 추출
        bookTitle = []
        bookScore = []
        bookAuthor = []
        bookPrice = []

        for j in bookCards:
            bookTitle.append(j.select_one(".title a").text)
            bookScore.append(j.select_one(".score").text)
            bookAuthor.append(j.select_one(".author").text)
            bookPrice.append(j.select_one(".sell_price").text)

        self.writeCSV(bookTitle, bookScore, bookAuthor, bookPrice)

    def writeCSV(self, Title, Score, Author, Price):
        file = open("kyobo.csv", "a", newline="")

        wr = csv.writer(file)
        for i in range(len(Title)):
            wr.writerow([str(i+1), Title[i], Score[i], Author[i], Price[i]])

        file.close()

    def scrap(self):

        file = open("kyobo.csv", "w", newline="")
        wr = csv.writer(file)
        wr.writerow(["No. ", "Title", "Score", "Author", "Price"])
        file.close()

        soupCard = self.getHTML()
        self.getCards(soupCard)

if __name__ == "__main__":
    s = Scrapper()
    s.scrap()

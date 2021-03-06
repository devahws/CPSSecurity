import requests
from bs4 import BeautifulSoup
import csv

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, uic
form_class = uic.loadUiType("indeed.ui")[0]

class Scrapper(QObject) :
    updated = pyqtSignal(int)

    def __init__(self, textBrowser):
        super().__init__()
        self.url = "https://kr.indeed.com/jobs?q=python"
        self.textBrowser = textBrowser

    def getHTML(self, cnt):
        res = requests.get(self.url + "&start=" + str(cnt * 10))

        if res.status_code != 200:
            print("request error : ", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getPages(self, soup):
        pages = soup.select(".pagination > a")
        return len(pages)

    def getCards(self, soup, cnt):
        jobCards = soup.find_all("div", class_="jobsearch-SerpJobCard")
        jobID = []
        jobTitle = []
        jobLocation = []

        for j in jobCards:
            jobID.append("https://kr.indeed.com/viewjob?jk=" + j["data-jk"])
            jobTitle.append(j.find("a").text.replace("\n", ""))
            if j.find("div", class_ = "location") != None:
                jobLocation.append(j.find("div", class_ = "location").text)
            elif j.find("span", class_ = "location") != None:
                jobLocation.append(j.find("span", class_="location").text)

        self.writeCSV(jobID, jobTitle, jobLocation, cnt)

    def writeCSV(self, ID, Title, Location, cnt):
        file = open("indeed.csv", "a", newline="")

        wr = csv.writer(file)
        for i in range(len(ID)):
            wr.writerow([str(i+1+(cnt*10)), ID[i], Title[i], Location[i]])

        file.close()

    def scrap(self):
        soupPage = self.getHTML(0)
        pages = self.getPages(soupPage)

        file = open("indeed.csv", "w", newline="")
        wr = csv.writer(file)
        wr.writerow(["No. ", "Link", "Title", "Location"])
        file.close()

        for i in range(pages):
           soupCard = self.getHTML(i)
           self.getCards(soupCard, i)
           print(i+1, "번째 페이지 Done")
           self.textBrowser.append("%d번째 페이지 Done" %(i+1))
           self.updated.emit(int((i+1)/pages)*100)


class WindowClass(QMainWindow, form_class):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

            # 자신의 크롤러 class 가져오기

            self.crawler = Scrapper(self.textBrowser)

            # Thread 적용
            self.thread = QThread()
            self.crawler.moveToThread(self.thread)
            self.thread.start()

            # 푸쉬 버튼과 자신의 크롤러 실행을 연결
            self.pushButton.clicked.connect(self.crawler.scrap)

            # set window title
            self.setWindowTitle("indeed crawler")

            # progressBar 시그널이 발생했을 때
            self.crawler.updated.connect(self.progressBarValue)
            self.progressBarValue(0)

        def progressBarValue(self, value):
            self.progressBar.setValue(value)



if __name__ == '__main__':
        app = QApplication(sys.argv)
        myWindow = WindowClass()
        myWindow.show()
        app.exec_()
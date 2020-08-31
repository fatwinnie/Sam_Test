import requests
import csv
import codecs
from bs4 import BeautifulSoup

url = 'http://127.0.0.1:8000/bug.html'
#url = 'http://127.0.0.1:8000/cgi-bin/message.py'
resp = requests.get(url)
resp.encoding='utf-8'
soup = BeautifulSoup(resp.text, 'html.parser')

Title = []
Content = []
Time = []
posts = soup.find_all("div", class_ = "container_history")
#posts = soup.find_all(attrs={'class':'container_history'})

for post in posts:
    Title.append(post.find("div", class_ = "history_title").p.string)
    Content.append(post.find("div", class_ = "history_content").p.string)
    Time.append(post.find("div", class_ = "history_time").p.string)
    #Title.append(post.p.string)
#print(Title)





# 開啟輸出的 CSV 檔案
with open('tingMsg.csv', 'w', newline='',encoding='utf_8') as csvfile:


    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile, Title)

    # 寫入一列資料
    writer.writerow(Title)
    writer.writerow(Content)
    writer.writerow(Time)


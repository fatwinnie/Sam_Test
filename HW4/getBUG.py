import requests
from bs4 import BeautifulSoup 
import csv
import mysql.connector

Title = []
Content = []
Time = []


def getData(url):
    my_header={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
        'cookie':'Cookie: POOH_SID=ba47332da89c5a95675360fb1c6f8c4c1df6842e'
    }
    resp = requests.get(url, headers= my_header)
    resp.encoding ='utf-8'
    #解析原始碼
    soup = BeautifulSoup(resp.text, 'lxml')
    find_title = soup.find_all("div",class_="history_title")
    fine_content = soup.find_all("div",class_= "history_content")
    find_time = soup.find_all("div",class_="history_time")
   
    for title in find_title:        
        Title.append(title.p.string)
    #print(Title)
   

    for content in fine_content:      
        Content.append(content.p.string)
    #print(Content)

    for time in find_time:
        Time.append(time.p.string)
    #print(Time)
   
    
def write_CSV():
    with open('tingMsg.csv', 'w', newline='',encoding='utf_8') as csvfile:
        writer = csv.writer(csvfile, Title)
        writer.writerow(Title)
        writer.writerow(Content)
        writer.writerow(Time)

def write_DB():
    conn = mysql.connector.connect(      
    host='localhost', # 主機名稱
    database='homework', # 資料庫名稱
    user='root',      # 帳號
    password='root',  # 密碼
    charset='utf8') 

    cursor = conn.cursor()
    if Title != []:
        for i in Title:
            print(i)
            #sql = "INSERT INTO crawler (title) VALUES (%s)"
            #val = i
            #cursor.execute(sql, val)
            #onn.commit()
            #conn.close()






if __name__	== '__main__':
    pageURL='http://127.0.0.1:8000/cgi-bin/message.py'
    getData(pageURL)
    write_CSV()
    write_DB()

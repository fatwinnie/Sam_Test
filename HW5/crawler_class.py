import requests
from bs4 import BeautifulSoup 
import csv
import mysql.connector
from mysql.connector import Error

Title = []
Content = []
Time = []

class SearchWEB:

    def getData(self,url):
        my_header={
            'User-Agent':'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
            
        }
        my_data = {
            'UserName': 'mickey',
            'pwd':'1234',
        }

        login_url = 'http://127.0.0.1:8000/cgi-bin/login.py'
        session = requests.Session()
        resp= session.post(login_url, headers = my_header , data = my_data)
        resp = session.get(url,headers= my_header)
        #resp = requests.get(url, headers= my_header)
        resp.encoding ='utf-8'
        #解析原始碼
        soup = BeautifulSoup(resp.text, 'lxml')
        find_title = soup.find_all("div",class_="history_title")
        find_content = soup.find_all("div",class_= "history_content")
        find_time = soup.find_all("div",class_="history_time")
        
        for title in find_title:        
            Title.append(title.p.string)
        #print(Title)
    
        for content in find_content:      
            Content.append(content.p.string)
        #print(Content)

        for time in find_time:
            Time.append(time.p.string)
        #print(Time)

   
    
    def write_CSV(self,Title,Content,Time):
        
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
        password='2033',  # 密碼
        charset='utf8') 

        cursor = conn.cursor()
        # 取 Title[]長度來得到每個list的迴圈次數
        a = len(Title)
        for i in range(a):           
            try:
                        
                sql = "INSERT INTO crawler (title, content,time) VALUES (%s, %s,%s);"
                val = (Title[i],Content[i],Time[i])
                #print(i)
                        
                cursor.execute(sql, val)
                #print(sql)
        
            except Error as e:
                print("資料庫連接失敗：", e)

        conn.commit()
        conn.close()
        

if __name__	== '__main__':
    pageURL='http://127.0.0.1:8000/cgi-bin/message.py'
    search_web = SearchWEB()
    search_web.getData(pageURL)
    search_web.write_CSV(Title,Content,Time)
    #search_web.write_DB()    
  

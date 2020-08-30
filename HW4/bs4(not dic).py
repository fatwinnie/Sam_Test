import requests 
from bs4 import BeautifulSoup
import numpy as np

url = "https://www.ptt.cc/bbs/joke/index.html"
response = requests.get(url)
html_doc = response.text # text 屬性就是 html檔案
soup = BeautifulSoup(response.text, "html.parser") 

post_author = [] #建立一個空的 list 放作者 id
recommend = [] # 放推文數
post_title = [] #放標題
post_date = [] #放貼文日期

posts = soup.find_all("div", class_ = "r-ent")
for post in posts:
    try:
        post_author.append(post.find("div", class_ = "author").string)
    except:
        post_author.append(np.nan)
    try: 
        post_title.append(post.find("a").string)
    except:
        post_titles.append(np.nan)
    try:
        post_date.append(post.find("div", class_ = "date").string)
    except:
        post_dates.append(np.nan)

find_recommend = soup.find_all("div", class_ = "nrec")
for rec in find_recommend:
    try:
        #recommend.append(post.find("span").string)
        recommend.append(int(rec.find("span").string))
    except:
        recommend.append(np.nan)
        
    
print(post_author)
print('------------------')
print(recommend)
print('------------------')
print(post_title)
print('------------------')
print(post_date)

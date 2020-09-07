import requests
from bs4 import BeautifulSoup 
def getData(url):

    my_header={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'cookie':'over18=1'
    }
    resp = requests.get(url, headers= my_header)
    resp.encoding ='utf-8'
    #解析原始碼
    soup = BeautifulSoup(resp.text, 'lxml')
    #print(soup.title.string)
    #find_title = soup.find("div",class_="title")
    find_title = soup.find_all("div",class_="title")
    for title in find_title:
        if title.a !=None: #如果標題包含ａ標籤（沒有被刪除），印出來
            print(title.a.string)
            
    #抓取上一頁的連結
    #找到內文是＜上頁的a標籤
    nextLink = soup.find("a",string="‹ 上頁")　
    #print(nextLink["href"])
    return nextLink['href']

pageURL='https://www.ptt.cc/bbs/Gossiping/index.html'

count = 0
#抓取三頁
while count < 3:

    pageURL = "https://www.ptt.cc"+ getData(pageURL)
    count += 1
#print(pageURL)

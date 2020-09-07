import requests
import csv
import codecs
from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/steamawards?snr=1_4_wintersale__winter2019-SteamAwards'
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64} AppleWebKit/537.36(KHTML, like Gecko) Chrome/65.0.3342.181 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
}

resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'

soup = BeautifulSoup(resp.text, 'html.parser')

div_tags = soup.select('.award_card_year + div')
name_tags = soup.select('.award_card_youvoted_txt + div')

fieldNames = []

for x in div_tags:
    fieldNames.append(x.text)

game_list = []
for x in name_tags:
    game_list.append(x.text)

# 開啟輸出的 CSV 檔案
with open('steam2019.csv', 'w', newline='',encoding='utf_8_sig') as csvfile:


    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile, fieldNames)

    # 寫入一列資料
    writer.writerow(fieldNames)

    # 寫入另外幾列資料
    writer.writerow(game_list)

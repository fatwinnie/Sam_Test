from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os,sys


pageURL = 'https://www.amazon.com/'
#search_URL = 'https://www.amazon.com/s?k=ultrawide+monitors&ref=nb_sb_noss_2'
searchURL_template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
search_text = 'ulttrawide monitor'
search_term = search_text.replace(' ','+')
#print(search_term)
searchURL = searchURL_template.format(search_term) # put search_term into search_URL_template to replace {}
#print(searchURL)

driver = webdriver.Firefox()
driver.get(searchURL)
#print(driver.page_source)
soup = BeautifulSoup(driver.page_source,'html.parser')
result = soup.find_all('div',{'data-component-type': 's-search-result'})
#driver.get(search_URL)

records = []
# list item 
for item in result:    
    Item_Name = item.h2.a.text.strip()
    #print(Item_Name)

    Item_URL = 'https://www.amazon.com' + item.h2.a['href']
    #print(Item_URL)
    try:
        Price  = item.find('span','a-offscreen').text
        print(Price)
    except AttributeError:
        print('no price')   
    
    Item_Star = item.find('i').text
    #print(Item_Star)

    ReviewCount = item.find('span',{'class':'a-size-base','dir':'auto'}).text
    #print(ReviewCount)
    result = (Item_Name, Price, Item_Star, ReviewCount, Item_URL)
    print(type(result))
    records.append(result)
 

# record as csv file
with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
    writer.writerows(records)




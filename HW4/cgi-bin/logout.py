#! /home/ting/My_test1/bin/python3

import os
import sys
import re
import string
import time
from http import cookies
import datetime
import mysql.connector
from mysql.connector import Error

def findSID(cookieStr):
    #print(cookieStr)
    #index_sid_start = cookieStr.find('RUBY_SID')
    #index_sid_end = cookieStr.find(';',index_sid_start)
    #focusStr = cookieStr[index_sid_start:index_sid_end]
    temp = cookieStr.split('=')
    SID_val = temp[1]
    #print(SID_val)
    return SID_val
   
def deleteSID(_sid):
    try:
        conn = mysql.connector.connect(      
            host='localhost', # 主機名稱
            database='homework', # 資料庫名稱
            user='root',      # 帳號
            password='2033')  # 密碼

        cursor = conn.cursor()
        
        #cursor.execute("DELETE FROM  user_verify WHERE SID =%s",(_sid))
        cursor.execute("DELETE FROM `user_verify`WHERE SID=%(SID)s;",{'SID':_sid})
        conn.commit()
        print('<h1>Logout ok , Bye!</h1>')
        print('<p>go to login page after 3 seconds</p>')
        print('<meta http-equiv="refresh" content="3; url=../index.html">')
        
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
        sys.exit( e)

    finally:
        if (conn.open):
            cursor.close()
            conn.close()

string_cookie = os.environ.get('HTTP_COOKIE')
sid_cookie = findSID(string_cookie)
expire = datetime.datetime.utcnow() 
format_expire = expire.strftime("%a, %d %b %Y %H:%M:%S GMT") 
print("Set-Cookie:POOH_SID=",sid_cookie,"; expires=",format_expire,"; Path=/cgi-bin/")

print("Content-Type:text/html; charset=utf-8")
print("") # end of header     
print(sid_cookie)
deleteSID(sid_cookie)

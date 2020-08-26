#! /usr/bin/python3

import os
import sys
import mysql.connector
from mysql.connector import Error
from http import cookies
import hashlib
import random
import string
from datetime import datetime, timedelta



def split(s:str,delimiter:str) -> list:
    s += delimiter # tricky
    start_pos = 0
    lst = []
    for i, ch in enumerate(s):
        if ch == delimiter:
            lst.append(s[start_pos:i])
            start_pos = i+1
    return lst


def hex_to_bin(hex:str) -> int:
    hex = hex.upper()
    ms_nibble = hex[0]
    ls_nibble = hex[1]

    def nibble_to_bin(ch:str) -> int:
        code = ord(ch)
        ret2 = (code - 0x30) if code < 0x41 else (code - 55)
        return ret2

    ret = nibble_to_bin(ms_nibble)*16 + nibble_to_bin(ls_nibble)
    return ret


def query_to_utf8(s:str, codec='utf8') -> str:
    i = 0
    length = len(s)
    bya = bytearray()
    while i < length:
        if s[i] == r'%':
            bya.append(hex_to_bin(s[i+1:i+3]))
            i += 3
        else:
            bya.append(ord(s[i]))
            i += 1
    return bya.decode(codec)


def query_components(s:str, codec='utf8') -> str:
    decode_str =  query_to_utf8(s,codec)
    pair_val_list = split(decode_str,'&')
    dic = {}
    for it in pair_val_list:
        key_val = split(it,'=')
        dic.update({key_val[0]:key_val[1]})
        
    return dic

def validate(_username,_password):
    global userData
    
    conn = mysql.connector.connect(      
        host='localhost', # 主機名稱
        database='homework', # 資料庫名稱
        user='root',      # 帳號
        password='root')  # 密碼

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM member WHERE name = %(name)s", {'name': _username})
    userData = cursor.fetchone()
   
    if userData is not None:

        if userData[2] == _password:
            #print(userData[1]) 
            return True
        else:
            return False
       

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def insertSID(_SID):
    global userData

    conn = mysql.connector.connect(      
    host='localhost', # 主機名稱
    database='homework', # 資料庫名稱
    user='root',      # 帳號
    password='root')  # 密碼

    #conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='10017730', db='ruby_db', charset='utf8')
    timeout = datetime.now() + timedelta(hours=1)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_verify (SID, user_ID, expire) VALUES (%s, %s, %s)" ,(_SID, userData[0],timeout ))
    conn.commit()

def findSID(cookieStr):
    temp = cookieStr.split('=')
    SID_val = temp[1]
    return SID_val
    



def update_SID_expire(_sid):
        
    conn = mysql.connector.connect(      
    host='localhost', # 主機名稱
    database='homework', # 資料庫名稱
    user='root',      # 帳號
    password='root')  # 密碼

    cursor = conn.cursor()
    cursor.execute("UPDATE user_verify SET expire = ADDTIME(CURRENT_TIMESTAMP,'2:0:0.0') WHERE SID = %s ",(_sid))
    conn.commit()


method = os.environ['REQUEST_METHOD']

if method =='GET':
    my_query = dict()
    my_query = query_components(os.environ['QUERY_STRING'])
    #print(my_query) ==> {'UserName': 'ting', 'pwd': '1234'} 
    #print(my_query['UserName']) ==> ting
  
    check = validate(my_query['UserName'],my_query['pwd'])
    if(check):
        print('Content-type:text/html;charset=UTF-8')
        print('')
        print('Welcome!')
        print('<meta http-equiv="refresh" content="2; url=./message.py">')
    else:
        print('Content-type:text/html;charset=UTF-8')
        print('')
        print('name or password Error!')
else:
    # method == POST
    post_len = int(os.environ['CONTENT_LENGTH'])
    detail = sys.stdin.read(post_len)
    post_dict = dict()
    post_dict = query_components(detail)
    #print(post_dict)

    if(validate(post_dict['UserName'],post_dict['pwd'])):
        print('Content-type:text/html;charset=UTF-8')
        str_cookie = os.environ.get('HTTP_COOKIE')
        
        if(str_cookie.find('POOH_SID')<0):
            token = hashlib.sha1() #hashlib提供字元加密功能
            token.update(get_random_string(50).encode('utf-8')) #產生隨機字串
            tokenCode = token.hexdigest()
            insertSID(tokenCode)
            print("Set-Cookie:POOH_SID=",tokenCode)

        else:
            SID_cookie = findSID(str_cookie)
            update_SID_expire(SID_cookie)

        print('')
        print('HELLO!!'+" "+post_dict['UserName'])      
        print('<meta http-equiv="refresh" content="2; url=./message.py">')

    else: 
        print('name or password Error!')
        print('<meta http-equiv="refresh" content="2; url=../index.html">')

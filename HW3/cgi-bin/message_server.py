#! /usr/bin/python3
import os
import sys
import mysql.connector
from mysql.connector import Error
import datetime

connection = mysql.connector.connect(
    host='localhost', # 主機名稱
    database='homework', # 資料庫名稱
    user='root',      # 帳號
    password='root')  # 密碼

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

print('Content-type:text/html;charset=UTF-8')
print('')
method = os.environ['REQUEST_METHOD']
if method =='POST':
    str_len = int(os.environ['CONTENT_LENGTH'])
    detail = sys.stdin.read(str_len)
    my_query = query_components(detail)
    #print(my_query)
    #print(my_query['title'])
    #now = datetime.datetime.utcnow()
    now = datetime.now().date()
    #print(now)

    if connection.is_connected():

        # inset into 資料庫
        cursor = connection.cursor() 
        sql = "INSERT INTO message (title,content,time) VALUES (%s, %s,%s)"
        val = (my_query['title'], my_query['content'],now.strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(sql, val)
        connection.commit()
        print('inserted successfully')
        print('<meta http-equiv="refresh" content="2;url=./message.py">')
       


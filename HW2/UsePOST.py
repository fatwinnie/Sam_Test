#! /usr/bin/python3

import os
import sys
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host='localhost', # 主機名稱
    database='test1', # 資料庫名稱
    user='root',      # 帳號
    password='2033')  # 密碼




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
   

    if connection.is_connected():
    # 查詢資料庫
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM member where name='{my_query['UserName']}';")
        row = cursor.fetchone()
        if row is None:
            print('name or password error')
            sys.exit()
        
    #print('hi')
    if my_query['pwd'] == row[2]:
        print('PASS!!!!!',"<BR>")
        print('Hi,',row[1],"<BR>")
        print('Your password is:',row[2])
    else:
        print('Password Error!')

    #my_query是dic{}，若要取password的值
    #要寫my_query['pwd'] 不是my_query[2]
    #括號放欲取值得'key值'

"""
while row is not None:
    print(row)
    row = cursor.fetchone()
"""
    

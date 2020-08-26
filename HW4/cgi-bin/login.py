#! /usr/bin/python3

import os
import sys
import mysql.connector
from mysql.connector import Error




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
    
        #conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='2033', db='test1', charset='utf8')
    conn = mysql.connector.connect(      
        host='localhost', # 主機名稱
        database='test1', # 資料庫名稱
        user='root',      # 帳號
        password='2033')  # 密碼

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM member WHERE name = %(name)s", {'name': _username})
    userData = cursor.fetchone()
   
    if userData is not None:
        if userData[2] == _password:
            #print(userData[1]) 
            return True
    else:
        #print('no data')
        return False
       
"""
        
    except Exception as e:
        print("Error: ", e)
        sys.exit( e)

    finally:
        if (conn.open):
            cursor.close()
            conn.close()
 """
    

print('Content-type:text/html;charset=UTF-8')
print('')
method = os.environ['REQUEST_METHOD']

if method =='GET':
    my_query = dict()
    my_query = query_components(os.environ['QUERY_STRING'])
    #print(my_query) ==> {'UserName': 'ting', 'pwd': '1234'} 
    #print(my_query['UserName']) ==> ting
    """ 原本寫的：
    query = os.environ['QUERY_STRING']   
    my_query = query_components(query)
    my_QueryName = my_query['UserName']     
    """
    check = validate(my_query['UserName'],my_query['pwd'])
    if(check):
        print('Welcome!')
        print('<meta http-equiv="refresh" content="2; url=./message.py">')
    else:
        print('name or password Error!')
else:
    post_len = int(os.environ['CONTENT_LENGTH'])
    detail = sys.stdin.read(post_len)
    post_dict = dict()
    post_dict = query_components(detail)
    #print(post_dict)
    if(validate(post_dict['UserName'],post_dict['pwd'])):
        print('HELLO!!'+" "+post_dict['UserName'])
        print('<meta http-equiv="refresh" content="2; url=./message.py">')
    else: 
        print('name or password Error!')
      


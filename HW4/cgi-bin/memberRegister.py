#! /home/ting/My_test1/bin/python3

import os
import sys
import mysql.connector
from mysql.connector import Error

import bcrypt
import random
from http import cookies

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

def insertUser(_name,_pwd):
    try:
        conn = mysql.connector.connect(      
        host='localhost', # 主機名稱
        database='homework', # 資料庫名稱
        user='root',      # 帳號
        password='2033')  # 密碼

        cursor = conn.cursor()
        salt = bcrypt.gensalt()
        hashPassword = bcrypt.hashpw(_pwd.encode(),salt)
        cursor.execute("INSERT INTO member (name, password, salt) VALUES (%s, %s, %s)" ,(_name,hashPassword,salt))
        conn.commit()

        #print('Content-type:text/html;charset=UTF-8')
        #print('')
        print('<p> Success </p>')
        print('<meta http-equiv="refresh" content="1; url=../index.html">')

    except Exception as e:
        conn.rollback()
        print('Error:',e)

    finally:
        cursor.close()
        conn.close()


print('Content-type:text/html;charset=UTF-8')
print('')
post_len = int(os.environ['CONTENT_LENGTH'])
#print(post_len)
posts = sys.stdin.read(post_len)
#print(posts)
post_dict = dict()
post_dict = query_components(posts)
#print(post_dict)
#print(post_dict['login_name'])

insertUser(post_dict['login_name'], post_dict['login_pass1'] )



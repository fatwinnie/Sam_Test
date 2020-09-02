#! /home/ting/My_test2/bin/python3
import os
import sys
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import random
import bcrypt
import hashlib
from http import cookies
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


def findSID(cookieStr):
    temp = cookieStr.split('=')
    SID_value = temp[1]
    return SID_value


def SID_info(_sid):

    conn = mysql.connector.connect(      
    host='localhost', # 主機名稱
    database='test1', # 資料庫名稱
    user='root',      # 帳號
    password='2033')  # 密碼

    cursor=conn.cursor()
    row_count=cursor.execute("SELECT user_ID FROM user_verify JOIN member \
        ON user_verify.user_ID=member.idmember WHERE `expire` > CURRENT_TIMESTAMP \
        AND user_verify.SID = %s",(_sid,))
    msg = cursor.fetchone()
    # 因為剛好遇到expire為保留字串，所以expire 要加上`expire`  
    # (_sid) 是trple()
    # 若要取第一個值，不能只寫(_sid_)，要寫(_sid,)  

    if msg is not None:
        return msg
    else:
        print('沒有權限，請先登入')
        print('<meta http-equiv="refresh" content="2; url=../index.html">')
        sys.exit()


def AddMessage(form_msg,user_ID):

    conn = mysql.connector.connect(      
    host='localhost', # 主機名稱
    database='test1', # 資料庫名稱
    user='root',      # 帳號
    password='2033')  # 密碼

    cursor = conn.cursor()
    sql = "INSERT INTO message (title,content,time,user_id) VALUES (%s,%s, %s,%s)"
    val = (form_msg['title'], form_msg['content'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_ID )
    cursor.execute(sql, val)
    conn.commit()


def history(userId):

    conn = mysql.connector.connect(      
    host='localhost', # 主機名稱
    database='test1', # 資料庫名稱
    user='root',      # 帳號
    password='2033')  # 密碼

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM message WHERE user_id= %(user_id)s", {'user_id': userId})
    report = cursor.fetchall()
     
    if report != []:
        for field in report:
            
            print('<div class="container_history">')
            print('<div class="history_title">')
            print(f'Title:<p>{field[2]}</p>')
            print('</div>')

            print('<div class="history_content">')
            print(f'content:<p>{field[3]}</p>')
            print('</div>')

            print('<div class="history_time">')
            print(f'post_time:<p>{field[4]}</p>')
            print('</div>')
            
            print('<hr/>')
            print('</div>')
    else:
        print('No history message in database')


    
string_cookie = os.environ.get('HTTP_COOKIE')
method = os.environ['REQUEST_METHOD']

if(string_cookie.find('POOH_SID')<0):
    print('Content-type:text/html;charset=UTF-8')
    print('') # end of header 
    print('<h1>你沒有權限，請先登入</h1>')
    print('<meta http-equiv="refresh" content="2; url=../index.html">')

else:
    print('Content-type:text/html;charset=UTF-8')
    print('') # end of header
    #print('hiii')
    sid_cookie = findSID(string_cookie)
    data = SID_info(sid_cookie)
    #print(data)

    if method=='POST':
        POSTstr_len = int(os.environ['CONTENT_LENGTH'])
        detail = sys.stdin.read(POSTstr_len)
        replace_detail = detail.replace('+','%20') #當按空白鍵 會變成+號,所以把+號轉換成％20
        my_query = query_components(replace_detail)
        AddMessage(my_query,data[0])
  

#print('Hi,',data[0]
print('<!DOCTYPE html> ')
print('<html>')
print('<head>')
print('<title>留言板</title>')
print('</head>')
print('<body>')
print('<div class="container">')
print(' <form action="./message.py" method="POST">')
print('     標題:<input type="text" name="title">',"<BR>")
print('     內容:',"<BR>")
print('     <TEXTAREA name="content" rows=6 cols=60></textarea>',"<BR>")
print('     <input type="submit" value="送出">')
print('</form>')
print('</div>')

print('<BR>')
print('<div class="container_history">')
print(' <h1>History Message</h1>')
print('</div>')

history(data[0])


print('</body>')
print('</html>')

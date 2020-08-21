#! /usr/bin/python3

import os
import sys


print('Content-type:text/html')
print('')
method = os.environ['REQUEST_METHOD']
if method =='GET':
    #print("GET","<BR>")
    query = os.environ['QUERY_STRING']
    #print(query)
    #print("<BR>")

MyQuery = query.split('&')
#print(MyQuery)
#print('<BR>')
#print(MyQuery[0])
UserName = MyQuery[0].split('=')
#print(UserName)
#print(UserName[1])
Passowrd = MyQuery[1].split('=')
#print(Passowrd)
#print(Passowrd[1])

if(UserName[1]=='ting' and Passowrd[1]=='1234'):
    print('<h1>PASS</h1>','<BR>')
    print('Hello',UserName[1],'<BR>')
    print('your password is:',Passowrd[1])
else:
    print('ERROR!!')

#! /usr/bin/python3

import os
import sys


len = int(os.environ['CONTENT_LENGTH'])
detail = sys.stdin.read(len)

print('Content-type:text/html')
print('')
#print('len= ',len,'<BR>') // len=22
#print(detail) // UserName=ting&pwd=1234 

MyQuery = detail.split('&') 
#print(MyQuery) // ['UserName=ting', 'pwd=1234'] 
UserName = MyQuery[0].split('=')
Passowrd = MyQuery[1].split('=')
#print(UserName) // ['UserName', 'ting']
#print(Password) // ['pwd','1234'] 
#print(UserName[1],Passowrd[1]) //UserName[1]=='ting'

if(UserName[1]=='ting' and Passowrd[1]=='1234'):
    print('<h1>PASS</h1>','<BR>')
    print('Hello',UserName[1],'<BR>')
    print('your password is:',Passowrd[1])
else:
    print('ERROR!!')

#! /usr/bin/python3

import os
import sys
import cgi

form = cgi.FieldStorage()    

name = form.getvalue('UserName')
password = form.getvalue('pwd')

print('Content-type:text/html')
print('')
#print(form)  
#FieldStorage(None, None, [MiniFieldStorage('UserName', 'ting'), MiniFieldStorage('pwd', '1234')]) 

if(name == 'ting' and password == '1234'):
    print('<h1>PASS</h1>') 
    print('Hello %s' % (name))
    print('<BR>')
    print('your password is: %s' %(password))
else:
    print('ERROR!!!')

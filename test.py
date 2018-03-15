# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:58:06 2017

@author: Air
"""

fi=open('AlldataTotal.txt','r')
count=0
c=0
while True:
    
    s=fi.readline()
    if s=='':
        break    
    a=s.split(' ')
    print a[0]
    if int(a[0])==1:
        count=count+1

print count

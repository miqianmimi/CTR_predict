# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:51:48 2017

@author: Air
"""
from sklearn.preprocessing import OneHotEncoder
 
print Totaldata
print unclick
print click

################ Wirte into the txt#####################
output = open('AlldataTotal.txt', 'w')
write=[]
line=[]
j=0
for j in range(len(Totaldata)):
    if j+1 in unclick:
        output.write(str(0))
    else:
        output.write(str(1))
    output.write(" ")
    i=0
    for i in range(len(Totaldata[j])):
        output.write(str(Totaldata[j][i]))
        output.write(":1")
        output.write(" ")
        i=i+1
    j=j+1
    output.write("\n")


        

#file=open('result.txt','r')
#file.write()               

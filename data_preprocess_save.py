# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:51:48 2017

@author: Air
"""
from sklearn.preprocessing import OneHotEncoder
 
fi=open('all_features.csv','r')
i=0
click=[]
unclick=[]
dataa=[]
while True:    
    line=fi.readline()
    if line=='':
        print i
        break
    s=line.split(',')
    count=0
    t=[]
    for j in s:
        #if i>=1 and count==0:
            #c=i-len(click)-len(unclick)-1
            #print c
        if i>=1 and count>=3 and count<=12:
            t.append(j)        
        if i>=1 and count==14 :
            dataa.append(t)
            #print j
            if int(j)==0:    
                unclick.append(i)
            else:
                click.append(i)
            #print len(click)    
            #print len(unclick)
            #print '\n'
        count=count+1    
    i=i+1
    
#print unclick
#print click



sizeofunclick=len(unclick)
sizeofclick=len(click)
print"没有点击的数据集够个数有%d" %(sizeofunclick)
print"点击过的数据有%d" %(sizeofclick)


enc = OneHotEncoder()
enc.fit(dataa)
print"enc.n_values_is:",enc.n_values_
print"enc.feature_indices_is:",enc.feature_indices_
print enc.transform([dataa[0]]).toarray()

########################Transform################################
Totaldata=[]
for i in range(len(dataa)):
    data= enc.transform([dataa[i]]).toarray()
    #print a
    size=len(data[0]) 
    #print size
    county=0
    datatransformed=[]
    for county in range(size):
        if data[0][county]==1:    
            datatransformed.append(county)
        county=county+1
    i=i+1
    if i%1000==0:
        print i
    Totaldata.append(datatransformed)
print "数据转换前的维度%d" %(size)
print "数据经过转换后的维度%d" %(len(datatransformed))
#print Totaldata

################ Wirte into the txt#####################
output = open('AlldataTotal1.txt', 'w')
write=[]
line=[]
j=0
for j in range(len(Totaldata)):
    if j+1 not in click:
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
    if j %1000==0:
        print j


        

#file=open('result.txt','r')
#file.write()               

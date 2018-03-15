# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:54:19 2017

@author: Air
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 16:11:41 2017

@author: Air
"""

#Sn=[]
#DTTime=[]
#Province=[]
City=[]
District=[]
Channel=[]
Domain=[] 
Slot=[]
Tag=[] 
Hour=[] 
Terminal=[] 
Agent=[] 
Material=[] 
#fltCPM=[] 
boolClick=[]


a=open('all_features.csv','r')
first=True
for line in a:
    s=line.strip().split(",")    
    if first:
        first=False
    else:
     #   Sn.append(s[0])
    #DTTime.append(s[1])
    #Province.append(s[2])
        City.append(s[3])
        District.append(s[4])
        Channel.append(s[5])
        Domain.append(s[6])
        Slot.append(s[7])
        Tag.append(s[8])
        Hour.append(s[9])
        Terminal.append(s[10])
        Agent.append(s[11])
        Material.append(s[12])
    #fltCPM.append(s[13])
        boolClick.append(int(s[14]))
a.close()
dim=0
T=['City','District','Channel','Domain','Slot','Tag','Hour','Terminal','Agent','Material']
for arr in T:
    dic={}
    arr1=eval(arr)
    i=0
    for item in arr1:
        dic[str(arr+':'+item)]=1
    print dic
    s=open('3indexnew.txt','a')
    for key in dic:
        s.write(str(key)+ '\t'+str(i+dim))
        s.write('\n')
        i=i+1
    print(len(dic))    
    dim=dim+len(dic)
    #print dim
    s.close()



print sum(boolClick)




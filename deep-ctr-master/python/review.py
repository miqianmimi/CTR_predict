# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 17:02:16 2017

@author: Air
"""

import pprint, pickle

pkl_file = open('mlp3fm_test_SmartCloud.p', 'rb')

data1 = pickle.load(pkl_file)
for i in data1:
    if i <0.5:
        print 0
    else :
        print 1

pprint.pprint(data1)

pkl_file.close()

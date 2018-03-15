# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 11:14:11 2017

@author: Air
"""
import sys
import time
import math
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
import features
global feature_cols,feature_cols_special,feature_index

def rewrite_train_test(input_file, rewrite_file):
    namecol = {}
    reader = open(input_file, 'r')
    writer = open(rewrite_file, 'w')
    first = True
    for line in reader:
        s = line.strip().split('\t')
        if first:
            first = False
            for i in range(1, len(s)):
                name = s[i]
                if name in feature_cols or name in feature_cols_special:
                    namecol[name] = i
            continue
        writer.write('%s,%.5f' % (s[0], w_0))
        fid = 1
        for name in feature_cols + feature_cols_special:
            i = namecol[name]
            feature = s[i]
            if name in feature_cols_special:
                feature = feat_trans(name, s[i])
            vfeat = np.zeros(k)
            wfeat = 0.
            if ',' in feature:
                tags = get_tags(feature)
                for tag in tags:
                    feature = name + ':' + tag
                    if feature not in feature_index:
                        feature = name + ':other'
                    idx = feature_index[feature]
                    vfeat += v[idx]
                    wfeat += w[idx]
                vfeat /= len(tags)
                wfeat /= len(tags)
            else:
                feature = name + ':' + feature
                if feature not in feature_index:
                    feature = name + ':other'
                idx = feature_index[feature]
                vfeat = v[idx]
                wfeat = w[idx]
            writer.write(',%.5f' % wfeat)
            #writer.write(' %d:%.5f' % (fid, wfeat))
            fid += 1
            for j in range(k):
                writer.write(',%.5f' % vfeat[j])
                #writer.write(' %d:%.5f' % (fid, vfeat[j]))
                fid += 1
        writer.write('\n')
    reader.close()
    writer.close()
    
    
a='featindex.fm.txt'
b='testoutput.txt'
rewrite_train_test(a,b)
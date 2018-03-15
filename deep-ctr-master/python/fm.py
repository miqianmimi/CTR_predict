#!/usr/bin/python
import sys
import time
import math
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
import features

def sigmoid(p):
    return 1.0 / (1.0 + math.exp(-p))

def pred_lr(x):
    p = w_0
    for (feat, val) in x:
        p += w[feat] * val
    p = sigmoid(p)
    return p

def pred(x):#this is the longest interaction function....2017.8.22.13:45
    p = w_0
    sum_1 = 0
    sum_2 = 0
    for (feat, val) in x:
        #print val
        tmp = v[feat] * val
        #print tmp
        sum_1 += tmp
        sum_2 += tmp * tmp
    p = np.sum(sum_1 * sum_1 - sum_2) / 2.0 + w_0
    for (feat, val) in x:
        p += w[feat] * val
    p = sigmoid(p)
    return (p, sum_1)

def one_data_y_x(line):
    s = line.strip().replace(':', ' ').split(' ')
    y = int(s[0])
    x = []
    for i in range(1, len(s), 2):
        #print i
        #print s[i]
        val = 1
        if not one_value:
            val = float(s[i+1])
        #print s[i]
        x.append((int(s[i]), val))
    #print x
    return (y, x)

def output_model(model_file):
    print 'output model to ' + model_file
    foo = open(model_file, 'w')
    foo.write('%.5f %d %d\n' % (w_0, feature_num, k))
    for i in range(feature_num):
        foo.write('%d %.5f' % (i, w[i]))
        for j in range(k):
            foo.write(' %.5f' % v[i][j])
        foo.write(' %s\n' % index_feature[i])
    foo.close()

def load_model(model_file):
    global feature_num, k, w_0, w, v, index_feature, feature_index
    print 'loading model from ' + model_file
    fi = open(model_file, 'r')
    line_num = 0
    for line in fi:
        line_num += 1
        s = line.strip().split()
        if line_num == 1:
            w_0 = float(s[0])
            feature_num = int(s[1])
            k = int(s[2])
            v = np.zeros((feature_num, k))
            w = np.zeros(feature_num)
            index_feature = {}
            feature_index = {}#intialize
        else:
            i = int(s[0])
            w[i] = float(s[1])
            for j in range(2, 2 + k):
                v[i][j-2] = float(s[j])#############################2017.8.22.???j-2
            feature = s[2 + k]
            index_feature[i] = feature
            feature_index[feature] = i
    fi.close()



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

# start here

if len(sys.argv) < 6:
    print 'Usage: train.fm.txt test.fm.txt feature_index_file result_file model_file | ' \
          '(optional) train.log.txt test.log.txt train.dl.txt test.dl.txt'
    exit(-1)
# global setting
np.random.seed(11)
one_value = True
k = 5
learning_rate = 0.01
weight_decay = 1E-6
v_weight_decay = 1E-6
train_rounds = 40
buffer_num = 1000000
modelalready=False


# initialise
feature_index = {}
index_feature = {}
max_feature_index = 0
feature_num = 0

print 'reading feature index'
fi = open(sys.argv[3], 'r')
for line in fi:
    s = line.strip().split('\t')
    index = int(s[1])
    #print index
    feature_index[s[0]] = index
    #print feature_index
    index_feature[index] = s[0]
    max_feature_index = max(max_feature_index, index)
fi.close()
feature_num = max_feature_index + 1
print 'feature number: ' + str(feature_num)

if modelalready:
    print'load model'
    print"intialising from a already trained model"
    load_model(sys.argv[5])

if not modelalready:
    print 'initialising without a model'
    init_weight = 0.05
    v = (np.random.rand(feature_num, k) - 0.5) * init_weight
    #print v
    w = np.zeros(feature_num)
    w_0 = 0

# train
best_auc = 0.
overfitting = False

print 'training for round :'
fo = open(sys.argv[4], 'w')
for round in range(1, train_rounds+1):
    start_time = time.time()
    fi = open(sys.argv[1], 'r')
    line_num = 0
    train_data = []   
    #myqtest=0
    while True:
        line = fi.readline().strip()   
        if len(line)>0: 
            line_num = (line_num + 1) % buffer_num
            train_data.append(one_data_y_x(line))
            #myqtest=myqtest+1
            #if myqtest%1000==0:
                #print myqtest
            #if myqtest>22310:
               # print line
               # print myqtest
        #print train_data
        if line_num == 0 or len(line) == 0:#complete reading data
            for data in train_data:
                y = data[0]
                x = data[1]
                # train one data
                #print x
                #print y
                (p, vsum) = pred(x)
                d = y - p
                #print d
                w_0 = w_0 * (1 - weight_decay) + learning_rate * d
                for (feat, val) in x:
                    w[feat] = w[feat] * (1 - weight_decay) + learning_rate * d * val
                for (feat, val) in x:
                    v[feat] = v[feat] * (1 - v_weight_decay) + learning_rate * d * (val * vsum - v[feat] * val * val)
            train_data = []
        if len(line) == 0:
            break
    #print w,v
    fi.close()
    train_time = time.time() - start_time
    train_min = int(train_time / 60)
    train_sec = int(train_time % 60)

    print" test for round "
    y = []
    yp = []
    fi = open(sys.argv[2], 'r')
    for line in fi:
        data = one_data_y_x(line)
        clk = data[0]
        pclk = pred(data[1])[0]
        y.append(clk)
        yp.append(pclk)
    fi.close()
    auc = roc_auc_score(y, yp)
    rmse = math.sqrt(mean_squared_error(y, yp))
    print '%d\t%.8f\t%.8f\t%dm%ds' % (round, auc, rmse, train_min, train_sec)
    fo.write('%d\t%.8f\t%.8f\t%dm%ds\n' % (round, auc, rmse, train_min, train_sec))
    logloss=0
    for i in range(len(yp)):
        if y[i]==0:    
            logloss=logloss+math.log(1-yp[i])
        if y[i]==1:
            logloss=logloss+math.log(yp[i])
    logloss=(-1)*logloss/len(yp)
    print "logloss"+"\t"+str(logloss)
    fo.write('logloss%.5f \n' %(logloss))
    fo.flush()
    if overfitting and auc < best_auc:
        if len(sys.argv) ==6:
            print 'output model into ' + sys.argv[5]
            output_model(sys.argv[5])
        if len(sys.argv) == 10:
            print 'rewriting ' + sys.argv[6] + ' into ' + sys.argv[8]
            rewrite_train_test(sys.argv[6], sys.argv[8])
            print 'rewriting ' + sys.argv[7] + ' into ' + sys.argv[9]
            rewrite_train_test(sys.argv[7], sys.argv[9])
            print 'output model into ' + sys.argv[5]
            output_model(sys.argv[5])
        break # stop training when overfitting two rounds already
    if auc > best_auc:
        best_auc = auc
        overfitting = False
    else:
        overfitting = True
fo.close()
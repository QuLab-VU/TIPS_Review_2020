#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:39:55 2019

@author: meyerct6
"""
import numpy as np
import pickle 
np.random.seed(1) #For reproducibility

norm = 'tanh'
test_fold = 0
val_fold = 1
        
def normalize(X, means1=None, std1=None, means2=None, std2=None, feat_filt=None, norm='tanh_norm'):
    if std1 is None:
        std1 = np.nanstd(X, axis=0)
    if feat_filt is None:
        feat_filt = std1!=0
    X = X[:,feat_filt]
    X = np.ascontiguousarray(X)
    if means1 is None:
        means1 = np.mean(X, axis=0)
    X = (X-means1)/std1[feat_filt]
    if norm == 'norm':
        return(X, means1, std1, feat_filt)
    elif norm == 'tanh':
        return(np.tanh(X), means1, std1, feat_filt)
    elif norm == 'tanh_norm':
        X = np.tanh(X)
        if means2 is None:
            means2 = np.mean(X, axis=0)
        if std2 is None:
            std2 = np.std(X, axis=0)
        X = (X-means2)/std2
        X[:,std2==0]=0
        return(X, means1, std1, means2, std2, feat_filt)  

#Train models
v = ['tr','val','train','test']
for e in v:
    file = open("data_X_"+e+".p",'rb')
    tmp = pickle.load(file)
    tmp, means1, std1, feat_filt = normalize(tmp, norm=norm)
    file.close()
    with open('data_X_'+e+'_norm.p','wb') as f:
        pickle.dump(tmp,f)
    with open('data_X_'+e+'_norm_features.p','wb') as f:
        pickle.dump([means1,std1,feat_filt],f)
    del tmp
    
with open("data_X_tr_norm.p",'rb') as f:
    X_tr = pickle.load(f)
with open("data_X_val_norm.p",'rb') as f:
    X_val = pickle.load(f)    
with open("data_X_train_norm.p",'rb') as f:
    X_train = pickle.load(f)    
with open("data_X_test_norm.p",'rb') as f:
    X_test = pickle.load(f)
with open("data_y_tr.p",'rb') as f:
    y_tr = pickle.load(f)
with open("data_y_val.p",'rb') as f:
    y_val = pickle.load(f)    
with open("data_y_train.p",'rb') as f:
    y_train = pickle.load(f)    
with open("data_y_test.p",'rb') as f:
    y_test = pickle.load(f)
    
pickle.dump((X_tr, X_val, X_train, X_test, y_tr, y_val, y_train, y_test), 
            open('data_test_fold%d_%s.p'%(test_fold, norm), 'wb'))




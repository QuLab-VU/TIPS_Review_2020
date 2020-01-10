#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:34:47 2019

@author: meyerct6
"""

#Data Manipulations
import pandas as pd 
import pickle
import numpy as np
import gzip 
import os
from shutil import copyfile

#Load fits caluclated from syn_calc.py
[iden,bliss,loewe,hsa] = pickle.load(open('syn_fits.p','rb'),encoding='latin1')

synMat = pd.DataFrame([loewe,bliss,hsa])
#Read in All the data used for fitting
file = gzip.open('X.p.gz', 'rb')
X = pickle.load(file)
file.close()

#contains synergy values and fold split (numbers 0-4)
labels = pd.read_csv('orig_labels.csv', index_col=0) 

#Save 3 pickle files with drug 1, drug 2, and cell line information
#Num drug features = 1309+802+2276   See Sec 2.1.2 of methods
numDfeat = 1309+802+2276
numCfeat = 3984

d1 = pd.DataFrame(X[0:len(labels),0:numDfeat])
d2 = pd.DataFrame(X[0:len(labels),numDfeat:2*numDfeat])
cl = pd.DataFrame(X[0:len(labels),2*numDfeat:])

d1 = d1.set_index(labels['drug_a_name']).drop_duplicates()
d2 = d2.set_index(labels['drug_b_name']).drop_duplicates()
cl = cl.set_index(labels['cell_line']).drop_duplicates()

pickle.dump([d1,d2,cl],open('drug_cell-line_features.p','wb'))
del d1
del d2
del cl

labels = pd.concat([labels, labels])
#Create folders for each synergy metric
synM = ['loewe','bliss','hsa']
for e,s in enumerate(synM):
    tmp = labels
    for ind in labels.index:
        tmp.loc[ind,'synergy'] = synMat.loc[e,iden.index(ind)]
    to_keep = (~tmp['synergy'].isna()) & (~np.isinf(tmp['synergy']))
    with open(s+'/X.p','wb') as f:
    	pickle.dump(X[to_keep,:],f,protocol=4)
    tmp = tmp[to_keep]
    tmp.to_csv(s+'/labels.csv')
    copyfile('cross_validation_step1.py',s+'/cross_validation_step1.py')
    copyfile('data_normalization_step1.py',s+'/data_normalization_step1.py')
    copyfile('data_normalization_step2.py',s+'/data_normalization_step2.py')
    copyfile('hyperparameters',s+'/hyperparameters')
    copyfile('prediction_step1.py',s+'/prediction_step1.py')
#labels are duplicated for the two different ways of ordering in the data

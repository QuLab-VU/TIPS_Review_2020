#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:52:42 2019

@author: meyerct6
"""

import numpy as np
import pandas as pd
import pickle 
np.random.seed(1) #For reproducibility

# in this example tanh normalization is used
# fold 0 is used for testing and fold 1 for validation (hyperparamter selection)
test_fold = 0
val_fold = 1
        
#contains the data in both feature ordering ways (drug A - drug B - cell line and drug B - drug A - cell line)
#in the first half of the data the features are ordered (drug A - drug B - cell line)
#in the second half of the data the features are ordered (drug B - drug A - cell line)
with open('X.p','rb') as f:
    X = pickle.load(f)

#contains synergy values and fold split (numbers 0-4)
labels = pd.read_csv('labels.csv', index_col=0) 
#labels are duplicated for the two different ways of ordering in the data

#indices of training data for hyperparameter selection: fold 2, 3, 4
idx_tr = np.where(np.logical_and(labels['fold']!=test_fold, labels['fold']!=val_fold))
#indices of validation data for hyperparameter selection: fold 1
idx_val = np.where(labels['fold']==val_fold)

#indices of training data for model testing: fold 1, 2, 3, 4
idx_train = np.where(labels['fold']!=test_fold)
#indices of test data for model testing: fold 0
idx_test = np.where(labels['fold']==test_fold)

#Create the data files for the next step to normalize.
X_tr = X[idx_tr]
with open('data_X_tr.p','wb') as f:
    pickle.dump(X_tr,f)
del X_tr

X_val = X[idx_val]
with open('data_X_val.p','wb') as f:
    pickle.dump(X_val,f)
del X_val

X_train = X[idx_train]
with open('data_X_train.p','wb') as f:
    pickle.dump(X_train,f)
del X_train

X_test = X[idx_test]
with open('data_X_test.p','wb') as f:
    pickle.dump(X_test,f)
del X_test

y_tr = labels.iloc[idx_tr]['synergy'].values
with open('data_y_tr.p','wb') as f:
    pickle.dump(y_tr,f)
del y_tr

y_val = labels.iloc[idx_val]['synergy'].values
with open('data_y_val.p','wb') as f:
    pickle.dump(y_val,f)
del y_val

y_train = labels.iloc[idx_train]['synergy'].values
with open('data_y_train.p','wb') as f:
    pickle.dump(y_train,f)
del y_train

y_test = labels.iloc[idx_test]['synergy'].values
with open('data_y_test.p','wb') as f:
    pickle.dump(y_test,f)
del y_test


    







        

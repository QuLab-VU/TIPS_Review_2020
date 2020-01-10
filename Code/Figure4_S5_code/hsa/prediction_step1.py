#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 08:20:22 2019

@author: meyerct6
"""

import pickle
import numpy as np
from tqdm import tqdm
import pandas as pd
import shap
from time import time
np.random.seed(1) #For reproducibility

with open('test_model.p','rb') as f:
    model = pickle.load(f)
    
with open('../drug_cell-line_features.p','rb') as f:
    [d1_feat,d2_feat,cl_feat] = pickle.load(f)
    
    
pred_bl_synergy = []
#For each sample do all possible interactions
cnt = 0
mat = np.nan*np.zeros(((len(d1_feat)*(len(d1_feat)-1)+1)*len(cl_feat),d1_feat.shape[1]+d2_feat.shape[1]+cl_feat.shape[1]))
lab = []

for sample in tqdm(cl_feat.index):
    #Create matrix:
    for d1 in d1_feat.index:
        for d2 in d2_feat.index:
            if d1!=d2:
                lab.append(d1+'_'+d2+'_'+sample)
                mat[cnt,:] = np.concatenate((d1_feat.loc[d1],d2_feat.loc[d2],cl_feat.loc[sample]))
                cnt+=1
                
with open('data_X_train_norm_features.p','rb') as f:
    [means1,std1,feat_filt] = pickle.load(f)
   
mat = mat[:,feat_filt]
#Normalize
mat = np.ascontiguousarray(mat)
mat = (mat-means1)/std1[feat_filt]
mat = np.tanh(mat)
with open("data_X_predict_norm.p",'wb') as f:
    pickle.dump(mat,f)  
tmp = model.predict(mat)

df = pd.DataFrame({'label':lab,'predicted':tmp.reshape((len(tmp),))})
mdf = pd.read_csv('labels.csv')

#merge based on labels
pdf = pd.merge(df,mdf,left_on = 'label',right_on='Unnamed: 0')          
import matplotlib.pyplot as plt
plt.figure()
plt.scatter(pdf['synergy'],pdf['predicted'])
plt.xlabel('Measured')
plt.ylabel('Predicted')
plt.title('Corr:%.2f'%pdf[['synergy','predicted']].corr().iloc[0,1])
plt.savefig('Correlation-predicted-measured.png')

df.to_csv('predicted.csv',index=False)

with open("data_X_train_norm.p",'rb') as f:
    X_train = pickle.load(f)   
#Feature Importance using SHAP
background = X_train[np.random.choice(X_train.shape[0], 1000, replace=False)]
e = shap.DeepExplainer(model,background)
##Estimate how long it is going to take:
#t=[]
#x = [10,20,50,100]
#for v in x:
#    t1 = time()
#    shap_vals = e.shap_values(mat[0:int(v),:])
#    t2 = time()
#    t.append(t2-t1)
#Results:
#LinregressResult(slope=0.3748955889623992, intercept=-0.4183295551611437, rvalue=0.9998875378635199, pvalue=0.00011246213648008488, stderr=0.0039760343619887634)
# 0.37*num_samp -.418

#Calculate the SHAP_values for the 100 most synergistic combinations according to the model
shap_vals = e.shap_values(mat[df.sort_values('predicted',ascending=False)[0:100].index,:])
with open("shap_vals.p",'wb') as f:
    pickle.dump(shap_vals[0],f)   
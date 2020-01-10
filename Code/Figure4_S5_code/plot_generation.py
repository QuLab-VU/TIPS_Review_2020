#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 11:20:22 2019

@author: meyerct6
"""
# =============================================================================
# Import packages
# =============================================================================
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *
import matplotlib.cm as cm
from matplotlib import rc
import glob
import numpy as np
import pandas as pd
import pickle
from matplotlib_venn import venn3
from matplotlib.ticker import FormatStrFormatter


rc('text', usetex=False)
font = {'family' : 'arial',
        'weight':'normal',
        'size'   : 8}
axes = {'linewidth': 2}
rc('font', **font)
rc('axes',**axes)

metrics  = ['bliss','loewe','hsa'] 
shap_vals = []; predicted = []
for m in metrics:
    shap_vals.append(pickle.load(open(m+'/shap_vals.p','rb')))
    predicted.append(list(pd.read_csv(m+'/predicted.csv').sort_values('predicted',ascending=False).iloc[0:1000,0]))
   
s = set(predicted[0]+predicted[1]+predicted[2])
idx1 = sum((~np.in1d(predicted[0],predicted[1]))&(~np.in1d(predicted[0],predicted[2])))
idx2 = sum((~np.in1d(predicted[1],predicted[0]))&(~np.in1d(predicted[1],predicted[2])))
idx3 = sum((~np.in1d(predicted[2],predicted[0]))&(~np.in1d(predicted[2],predicted[1])))

idx4 = sum((np.in1d(predicted[0],predicted[1]))&(~np.in1d(predicted[0],predicted[2])))
idx5 = sum((np.in1d(predicted[0],predicted[2]))&(~np.in1d(predicted[0],predicted[1])))
idx6 = sum((np.in1d(predicted[1],predicted[2]))&(~np.in1d(predicted[1],predicted[0])))

idx7 = sum((np.in1d(predicted[0],predicted[1]))&(np.in1d(predicted[0],predicted[2])))



ttt = set(predicted[0]) & set(predicted[1]) & set(predicted[2])
df = pd.DataFrame({'index':np.ones(len(ttt))})
df.index = ttt

for m in metrics:
    df[m+'_idx']=0.
    tmp = list(pd.read_csv(m+'/predicted.csv').sort_values('predicted',ascending=False).iloc[0:1000,0])
    for l in ttt:
        df.loc[l,m+'_idx'] = tmp.index(l)
df['mean'] = df[['bliss_idx','loewe_idx','hsa_idx']].mean(axis=1)
df = df.sort_values(by='mean')
df.iloc[0]


# =============================================================================
# Plot venn diagram, Figure 4
# =============================================================================

plt.figure()
venn3(subsets=(idx1,idx2,idx4,idx3,idx5,idx6,idx7))
plt.savefig('overlap_synPredictions.pdf',bbox_inches=0.)
#print the top 5 combinations by each metric
for m in metrics:
    tmp = list(pd.read_csv(m+'/predicted.csv').sort_values('predicted',ascending=False).reset_index().loc[0:4,'label'])
    for e,i in enumerate(tmp):
        print(str(e+1)+'. '+i.split('_')[0].lower()+'+'+i.split('_')[1].lower()+' in '+i.split('_')[2])
    
    
# =============================================================================
# Figure S5    
# =============================================================================

#Now for the feature bar plot
plt.figure(figsize=(3,5))
mth = 'loewe'#sort by
sv = np.mean(shap_vals[metrics.index(mth)],axis=0)
with open('loewe/data_X_train_norm_features.p','rb') as f:
    [means1,std1,feat_filt] = pickle.load(f)

#Num drug features = 1309+802+2276   See Sec 2.1.2 of methods
numDfeat = 1309+802+2276
numCfeat = 3984
numDfeat = sum(feat_filt[range(numDfeat)])
numCfeat = sv.shape[0]-numDfeat
drug_feat = sv[0:numDfeat]
cell_feat = sv[numDfeat:]

dindx = np.argsort(drug_feat)
cindx = np.argsort(cell_feat)
#
#dindx = np.concatenate((dindx[0:100],dindx[-100:]))
#cindx = np.concatenate((cindx[0:100],cindx[-100:]))

ax1 = plt.subplot(311)
ax1.bar(range(len(dindx)),[drug_feat[i] for i in dindx],edgecolor=None,alpha=.75,color='b',width=1,label=mth)

ax2 = plt.subplot(312)
mth = 'bliss'
sv = np.mean(shap_vals[metrics.index(mth)],axis=0)
drug_feat = sv[0:numDfeat]
cell_feat = sv[numDfeat:]
ax2.bar(range(len(dindx)),[drug_feat[i] for i in dindx],edgecolor=None,alpha=.75,color='r',width=1,label=mth)

ax3 = plt.subplot(313)
mth = 'hsa'
sv = np.mean(shap_vals[metrics.index(mth)],axis=0)
drug_feat = sv[0:numDfeat]
cell_feat = sv[numDfeat:]
ax3.bar(range(len(dindx)),[drug_feat[i] for i in dindx],edgecolor=None,alpha=.75,color='g',width=1,label=mth)

ax1.set_xticks([])
ax2.set_xticks([])
ax3.set_xticks([])

ax1.set_ylabel('Mean SHAP Value')
ax1.set_title('Loewe')
ax2.set_title('Bliss')
ax3.set_title('HSA')
ax3.set_xlabel('Drug Feature (Ordered by Loewe SHAP value)')

ax1.set_yticks([ax1.get_ylim()[0],0,ax1.get_ylim()[1]])
ax2.set_yticks([ax2.get_ylim()[0],0,ax2.get_ylim()[1]])
ax3.set_yticks([ax3.get_ylim()[0],0,ax3.get_ylim()[1]])

ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax3.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))

plt.tight_layout()
plt.savefig('Drug_FeatureImportance.pdf',bbox_inches=0.)


#Now for the feature bar plot
plt.figure(figsize=(3,5))
mth = 'loewe'#sort by
sv = np.mean(shap_vals[metrics.index(mth)],axis=0)
with open('loewe/data_X_train_norm_features.p','rb') as f:
    [means1,std1,feat_filt] = pickle.load(f)

#Num drug features = 1309+802+2276   See Sec 2.1.2 of methods
numDfeat = 1309+802+2276
numCfeat = 3984
numDfeat = sum(feat_filt[range(numDfeat)])
numCfeat = sv.shape[0]-numDfeat
drug_feat = sv[0:numDfeat]
cell_feat = sv[numDfeat:]

print(numDfeat)
print(numCfeat)

dindx = np.argsort(drug_feat)
cindx = np.argsort(cell_feat)
#
#dindx = np.concatenate((dindx[0:100],dindx[-100:]))
#cindx = np.concatenate((cindx[0:100],cindx[-100:]))

ax1 = plt.subplot(311)
ax1.bar(range(len(cindx)),[cell_feat[i] for i in cindx],edgecolor=None,alpha=.75,color='b',width=1,label=mth)

ax2 = plt.subplot(312)
mth = 'bliss'
sv = np.mean(shap_vals[metrics.index(mth)],axis=0)
drug_feat = sv[0:numDfeat]
cell_feat = sv[numDfeat:]
ax2.bar(range(len(cindx)),[cell_feat[i] for i in cindx],edgecolor=None,alpha=.75,color='r',width=1,label=mth)

ax3 = plt.subplot(313)
mth = 'hsa'
sv = np.mean(shap_vals[metrics.index(mth)],axis=0)
drug_feat = sv[0:numDfeat]
cell_feat = sv[numDfeat:]
ax3.bar(range(len(cindx)),[cell_feat[i] for i in cindx],edgecolor=None,alpha=.75,color='g',width=1,label=mth)

ax1.set_xticks([])
ax2.set_xticks([])
ax3.set_xticks([])

ax1.set_ylabel('Mean SHAP Value')
ax1.set_title('Loewe')
ax2.set_title('Bliss')
ax3.set_title('HSA')
ax3.set_xlabel('Cell Feature (Ordered by Loewe SHAP value)')

ax1.set_yticks([ax1.get_ylim()[0],0,ax1.get_ylim()[1]])
ax2.set_yticks([ax2.get_ylim()[0],0,ax2.get_ylim()[1]])
ax3.set_yticks([ax3.get_ylim()[0],0,ax3.get_ylim()[1]])

ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax3.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))

plt.tight_layout()

plt.savefig('CellLine_FeatureImportance.pdf',bbox_inches=0.)



#Correlation Rank Order
from scipy.stats import spearmanr

mth = 'loewe'#sort by
sv = np.mean(shap_vals[metrics.index(mth)],axis=0)
with open('loewe/data_X_train_norm_features.p','rb') as f:
    [means1,std1,feat_filt] = pickle.load(f)

#Num drug features = 1309+802+2276   See Sec 2.1.2 of methods
numDfeat = 1309+802+2276
numCfeat = 3984
numDfeat = sum(feat_filt[range(numDfeat)])
numCfeat = sv.shape[0]-numDfeat
drug_feat = sv[0:numDfeat]
cell_feat = sv[numDfeat:]

dindx = np.argsort(drug_feat)
cindx = np.argsort(cell_feat)


mth = ['bliss','hsa']
for m in mth:
    sv = np.mean(shap_vals[metrics.index(m)],axis=0)
    drug_feat1 = sv[0:numDfeat]
    drug_feat1 = [drug_feat1[i] for i in dindx]
    cell_feat1 = sv[numDfeat:]
    cell_feat1 = [cell_feat1[i] for i in cindx]

    print('%.2f'%spearmanr(drug_feat,drug_feat1).correlation)

    print('%.2f'%spearmanr(cell_feat,cell_feat1).correlation)





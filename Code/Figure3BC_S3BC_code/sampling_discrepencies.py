#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:02:23 2019

@author: meyerct6
"""
# =============================================================================
# Import packages
# =============================================================================
#Import packages
import pandas as pd     
import numpy as np
import os
#Figures
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *
import matplotlib.cm as cm
from matplotlib import rc
rc('text', usetex=False)
font = {'family' : 'arial',
        'weight':'normal',
        'size'   : 8}
axes = {'linewidth': 2}
rc('font', **font)
rc('axes',**axes)
from gatherData import subset_data, subset_expt_info

# =============================================================================
# Read in data
# =============================================================================
#Read in MuSyC fit to anti-malarial data
df = pd.read_csv('../../Data/Figure2_data/MasterResults_mcnlls.csv')
df['barcode'] = df['drug1_name']+'_'+df['drug2_name']+'_'+df['sample']

#Find what the mean of SynergyFinder is for bliss and loewe
for m in ['bliss','loewe']:
    for k in range(3):
        df['synF_'+m+'_sub'+str(k+1)] = np.nan

df['synF_mean_bliss'] = np.nan; df['synF_mean_loewe'] = np.nan

for i in df.index:
    f = df['barcode'].loc[i]
    for mth in ['Bliss','Loewe']:
        syF = '../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv'
        if os.path.isfile(syF):
            df_synF = pd.read_csv(syF,index_col=0,header=0)
            df_synF = df_synF.iloc[1:,1:]
            df_synF.index = range(len(df_synF))
            df_synF.columns = range(len(df_synF.T)) 
            if mth=='Bliss':
                #Bliss
                df.loc[i,'synF_bliss_sub1'] = df_synF.iloc[2,2]
                df.loc[i,'synF_bliss_sub2'] = df_synF.iloc[5,5]
                df.loc[i,'synF_bliss_sub3'] = df_synF.iloc[8,8]
                df.loc[i,'synF_mean_bliss'] = df_synF.mean().mean() 
            else:
                #Loewe
                df.loc[i,'synF_loewe_sub1'] = df_synF.loc[1,1]
                df.loc[i,'synF_loewe_sub2'] = df_synF.loc[4,4]
                df.loc[i,'synF_loewe_sub3'] = df_synF.loc[7,7]
                df.loc[i,'synF_mean_loewe'] = df_synF.mean().mean()

# =============================================================================
# Bliss example
# =============================================================================
#Find an example in bliss where 3 sampling points are all antagonistic but synergistic by the mean of the surface
df[((df[['synF_bliss_sub1','synF_bliss_sub2','synF_bliss_sub3']]<-1).all(axis=1)) & (df['synF_mean_bliss']>0) & (df['R2']>.95)][['synF_bliss_sub1','synF_bliss_sub2','synF_bliss_sub3','synF_mean_bliss']]
#Index of example
i = 770 # amodiaquine_artemether_PLASMODIUM_FALCIPARUM_HB3
f = df['barcode'].loc[i]
mth = 'Bliss'
syF = '../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv'
if os.path.isfile(syF):
    df_synF = pd.read_csv('../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv',index_col=0,header=0)
    df_synF = df_synF.iloc[1:,1:]
    df_synF.index = range(len(df_synF))
    df_synF.columns = range(len(df_synF.T))

data = pd.read_csv('../../Data/Figure2_data/'+df['expt'].loc[i])
data['drug1'] = data['drug1'].str.lower()
data['drug2'] = data['drug2'].str.lower()
data['sample'] = data['sample'].str.upper()
drug1_name = df.loc[i,'drug1_name']
drug2_name = df.loc[i,'drug2_name']
sample = df.loc[i,'sample']
d1,d2,dip,dip_sd = subset_data(data,drug1_name,drug2_name,sample)
drug1_units, drug2_units, expt_date = subset_expt_info(data,drug1_name,drug2_name,sample)
#Make the matrix
ud1 = np.unique(d1)
ud2 = np.unique(d2)
udip = np.nan*np.zeros(len(ud1)*len(ud2))
cnt=0
for i in range(len(ud1)):
    for j in range(len(ud2)):
        udip[cnt] = np.nanmean(dip[(d1==ud1[i])&(d2==ud2[j])])
        cnt+=1
DD1,DD2 = np.meshgrid(ud1,ud2)
mdip = udip.reshape(DD1.shape).T

data = pd.DataFrame(mdip)
data.columns = list(ud1)
data.index = list(ud2)

# =============================================================================
# Make Figure 3B,C
# =============================================================================

fig = plt.figure(figsize=(7,4))
ax = []
ax.append(plt.subplot2grid((10,2),(0,0),rowspan=7))
ax.append(plt.subplot2grid((10,2),(0,1),rowspan=7))
cax = []
cax.append(plt.subplot2grid((10,2),(8,0),rowspan=1))
cax.append(plt.subplot2grid((10,2),(8,1),rowspan=1))
plt.subplots_adjust(wspace=0,hspace=0.)
plt.sca(ax[0])
cmap = cm.cool_r
cmap.set_bad('white',1.)
plt.imshow(data, vmin=0,vmax=115.,origin='lower',cmap=cmap)
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].set_ylabel('log('+drug2_name+')',labelpad=-10)
ax[0].set_xlabel('log('+drug1_name+')',labelpad=-10)
ax[0].set_title('Percent Effect\nP. Falciparum Strain (HB3)')
cb = plt.colorbar(cax=cax[0],orientation='horizontal')
cb.set_ticks((0,100))
ax[0].set_xticks([0.])
ax[0].set_yticks([0.])

for r in range(len(data)):
    for c in range(len(data.T)):
        text = ax[0].text(c,r,int(np.round(data.iloc[r,c])),ha='center',va='center',color='w',fontsize=7)

df_synF.insert(0,-1,np.nan)
tmp = df_synF.T 
tmp.insert(0,-1,np.nan)
df_synF = tmp.T

plt.sca(ax[1])
cmap = cm.seismic
cmap.set_bad('gray',1.)
plt.imshow(df_synF, vmin=-85,vmax=85.,origin='lower',cmap=cmap)
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_ylabel('',labelpad=-10)
ax[1].set_xlabel('',labelpad=-10)
ax[1].set_title('SynergyFinder (Bliss)\n'+'Overall Mean:'+str(np.round(df_synF.mean().mean(),decimals=2)))
cb = plt.colorbar(cax=cax[1],orientation='horizontal')
cb.set_ticks((-50,0,50))

for r,c in zip((2,5,8),(2,5,8)):
    text = ax[1].text(c+1,r+1,np.round(df_synF.loc[r,c]),ha='center',va='center',color='k',fontsize=10,weight='bold')
fig.savefig('bliss_sampling_example.pdf',bbox_inches=0.)



# =============================================================================
# Loewe example
# =============================================================================
#Specific example
df[((df[['synF_loewe_sub1','synF_loewe_sub2','synF_loewe_sub3']]<-1).all(axis=1)) & (df['synF_mean_loewe']>0) & (df['R2']>.95)][['synF_loewe_sub1','synF_loewe_sub2','synF_loewe_sub3','synF_mean_loewe']]

i = 259 # bix01294_amodiaquine_PLASMODIUM_FALCIPARUM_3D7
f = df['barcode'].loc[i]
mth = 'Loewe'
syF = '../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv'
if os.path.isfile(syF):
    df_synF = pd.read_csv('../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv',index_col=0,header=0)
    df_synF = df_synF.iloc[1:,1:]
    df_synF.index = range(len(df_synF))
    df_synF.columns = range(len(df_synF.T))

from gatherData import subset_data, subset_expt_info
data = pd.read_csv('../../Data/Figure2_data/'+df['expt'].loc[i])
data['drug1'] = data['drug1'].str.lower()
data['drug2'] = data['drug2'].str.lower()
data['sample'] = data['sample'].str.upper()
drug1_name = df.loc[i,'drug1_name']
drug2_name = df.loc[i,'drug2_name']
sample = df.loc[i,'sample']
d1,d2,dip,dip_sd = subset_data(data,drug1_name,drug2_name,sample)
drug1_units, drug2_units, expt_date = subset_expt_info(data,drug1_name,drug2_name,sample)
#Make the matrix
ud1 = np.unique(d1)
ud2 = np.unique(d2)
udip = np.nan*np.zeros(len(ud1)*len(ud2))
cnt=0
for i in range(len(ud1)):
    for j in range(len(ud2)):
        udip[cnt] = np.nanmean(dip[(d1==ud1[i])&(d2==ud2[j])])
        cnt+=1
DD1,DD2 = np.meshgrid(ud1,ud2)
mdip = udip.reshape(DD1.shape).T


# =============================================================================
# Make Figure S3B,C
# =============================================================================
fig = plt.figure(figsize=(7,4))
ax = []
ax.append(plt.subplot2grid((10,2),(0,0),rowspan=7))
ax.append(plt.subplot2grid((10,2),(0,1),rowspan=7))
cax = []
cax.append(plt.subplot2grid((10,2),(8,0),rowspan=1))
cax.append(plt.subplot2grid((10,2),(8,1),rowspan=1))
plt.subplots_adjust(wspace=0,hspace=0.)
plt.sca(ax[0])
cmap = cm.cool_r
cmap.set_bad('white',1.)
plt.pcolormesh(DD1,DD2,mdip, vmin=0,vmax=115.,cmap=cmap)
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].set_ylabel(drug2_name,labelpad=-10)
ax[0].set_xlabel(drug1_name,labelpad=-10)
ax[0].set_title('Percent Effect\nP. Falciparum Strain (HB3)')
cb = plt.colorbar(cax=cax[0],orientation='horizontal')
cb.set_ticks((0,100))
ax[0].set_xticks([0.])
ax[0].set_yticks([0.])

for e1,v1 in enumerate(ud1[0:-1]+np.diff(ud1)/2.):
    for e2,v2 in enumerate(ud2[0:-1]+np.diff(ud2)/2.):
        text = ax[0].text(v1,v2,int(np.round(mdip[e1+1,e2+1])),ha='center',va='center',color='w',fontsize=7)

plt.sca(ax[1])
cmap = cm.seismic
cmap.set_bad('gray',1.)
plt.pcolormesh(DD1,DD2,df_synF, vmin=-50,vmax=50.,cmap=cmap)
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_ylabel('',labelpad=-10)
ax[1].set_xlabel('',labelpad=-10)
ax[1].set_title('SynergyFinder (loewe)\n'+'Overall Mean:'+str(np.round(df_synF.mean().mean(),decimals=2)))
cb = plt.colorbar(cax=cax[1],orientation='horizontal')
cb.set_ticks((-25,0,25))

ud1 = ud1[0:-1]+np.diff(ud1)/2.
ud2 = ud2[0:-1]+np.diff(ud2)/2.

for r,c in zip((1,4,7),(1,4,7)):
    text = ax[1].text(ud1[c],ud2[r],int(np.round(df_synF.loc[r,c])),ha='center',va='center',color='k',fontsize=10,weight='bold',clip_on=False)
plt.savefig('loewe_sampling_example.pdf',bbox_inches=0.)


# =============================================================================
# Old code for showing the concordance between different sampling locations
# =============================================================================


# from matplotlib_venn import venn3
# #Venn Diagrams
# plt.figure()
# plt.subplot(121)
# x1 = np.round(sum((df['synF_bliss_sub1']>0) & (df['synF_bliss_sub2']<0) & (df['synF_bliss_sub3']<0))/float(len(df)),2)*100.
# x2 = np.round(sum((df['synF_bliss_sub1']<0) & (df['synF_bliss_sub2']>0) & (df['synF_bliss_sub3']<0))/float(len(df)),2)*100.
# x3 = np.round(sum((df['synF_bliss_sub1']>0) & (df['synF_bliss_sub2']>0) & (df['synF_bliss_sub3']<0))/float(len(df)),2)*100.
# x4 = np.round(sum((df['synF_bliss_sub1']<0) & (df['synF_bliss_sub2']<0) & (df['synF_bliss_sub3']>0))/float(len(df)),2)*100.
# x5 = np.round(sum((df['synF_bliss_sub1']>0) & (df['synF_bliss_sub2']<0) & (df['synF_bliss_sub3']>0))/float(len(df)),2)*100.
# x6 = np.round(sum((df['synF_bliss_sub1']<0) & (df['synF_bliss_sub2']>0) & (df['synF_bliss_sub3']>0))/float(len(df)),2)*100.
# x7 = np.round(sum((df['synF_bliss_sub1']>0) & (df['synF_bliss_sub2']>0) & (df['synF_bliss_sub3']>0))/float(len(df)),2)*100.
# v = venn3(subsets = [int(i) for i in (x1,x2,x3,x4,x5,x6,x7)],set_labels = ('Sampling A','Sampling B','Sampling C'))


# plt.subplot(122)
# x1 = np.round(sum((df['synF_loewe_sub1']>0) & (df['synF_loewe_sub2']<0) & (df['synF_loewe_sub3']<0))/float(len(df)),2)*100.
# x2 = np.round(sum((df['synF_loewe_sub1']<0) & (df['synF_loewe_sub2']>0) & (df['synF_loewe_sub3']<0))/float(len(df)),2)*100.
# x3 = np.round(sum((df['synF_loewe_sub1']>0) & (df['synF_loewe_sub2']>0) & (df['synF_loewe_sub3']<0))/float(len(df)),2)*100.
# x4 = np.round(sum((df['synF_loewe_sub1']<0) & (df['synF_loewe_sub2']<0) & (df['synF_loewe_sub3']>0))/float(len(df)),2)*100.
# x5 = np.round(sum((df['synF_loewe_sub1']>0) & (df['synF_loewe_sub2']<0) & (df['synF_loewe_sub3']>0))/float(len(df)),2)*100.
# x6 = np.round(sum((df['synF_loewe_sub1']<0) & (df['synF_loewe_sub2']>0) & (df['synF_loewe_sub3']>0))/float(len(df)),2)*100.
# x7 = np.round(sum((df['synF_loewe_sub1']>0) & (df['synF_loewe_sub2']>0) & (df['synF_loewe_sub3']>0))/float(len(df)),2)*100.
# v = venn3(subsets = [int(i) for i in (x1,x2,x3,x4,x5,x6,x7)],set_labels = ('Sampling X','Sampling Y','Sampling Z'))
# plt.savefig('venn_diagrams.pdf',bbox_inches=0.)


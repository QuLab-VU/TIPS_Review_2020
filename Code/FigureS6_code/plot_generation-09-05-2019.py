#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 13:44:13 2019

@author: meyerct6
"""

import seaborn as sns
import numpy as np
import pandas as pd
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

T = pd.read_csv('../../Data/Figure5_data/katzir_2019/katzirAFFECT_synergy.csv')
T = T[T['num_drugs']>1.]
fig = plt.figure(figsize=(7,2))
ax = []
ax.append(plt.subplot(121))
sub_T = T[~T['loewe'].isin([np.nan, np.inf, -np.inf])]
#sns.stripplot(x='num_drugs',y='loewe',data=sub_T,ax=axes,jitter=.2,hue='sample',size=3,alpha=.1)
sns.violinplot('num_drugs','loewe',data=sub_T,ax=ax[0],palette=sns.color_palette("Blues",n_colors=int(sub_T['num_drugs'].max())),inner=None)
plt.scatter(plt.xticks()[0],sub_T.groupby(by='num_drugs')['loewe'].mean().values,5,'k')
ax[0].set_ylim([-1,1])
xlim = ax[0].get_xlim()
plt.hlines(0,xlim[0],xlim[1],'r')
ax[0].set_xlim(xlim)
ax[0].set_yticks([-1.,0,1])
ax[0].set_xlabel('Number of Drugs')
ax[0].set_ylabel('<----Ant   -log(Loewe)   Syn --->')

ax.append(plt.subplot(122))
sub_T = T[~T['bliss'].isin([np.nan, np.inf, -np.inf])]
sns.violinplot('num_drugs','bliss',data=sub_T,ax=ax[1],palette=sns.color_palette("Reds",n_colors=int(sub_T['num_drugs'].max())),inner=None)
plt.scatter(plt.xticks()[0],sub_T.groupby(by='num_drugs')['bliss'].mean().values,5,'k')
ax[1].set_ylim([-1,1])
xlim = ax[1].get_xlim()
plt.hlines(0,xlim[0],xlim[1],'r')
ax[1].set_xlim(xlim)
ax[1].set_yticks([-1.,0,1])
ax[1].set_xlabel('Number of Drugs')
ax[1].set_ylabel('<----Ant   Bliss   Syn --->')
plt.tight_layout()

fig.savefig('katzirAFFECT_higherOrderTrends.pdf',bbox_inches=0.)

# =============================================================================
# Look at fitted emax distribution
# =============================================================================
#Now calculate synergy based on percent AFFECT
T = pd.read_csv('../../Data/Figure5_data/katzir_2019/katzir_data_reformatted.csv')
# =============================================================================
# Now for each drug-sample single pair fit a hill curve to calculate the synergy
# =============================================================================
from fit_code import fit_drc,ll4,ll4_inv
#Bounds for the fitting equation
E_fix = None;E_bnd = [[.99,0.],[1.01,1.]]
E_fx = [np.nan,np.nan] if E_fix is None else E_fix; E_bd = [[-np.inf,-np.inf],[np.inf,np.inf]] if E_bnd is None else E_bnd
T['sample'] = T['sample']+'_'+T['expt']
samples = T['sample'].unique()
#Unique samples
T['bliss'] = np.nan;  T['num_drugs'] = 0; T['loewe'] = np.nan;
#For every experiment
        
emx1=[]    
for s in samples:
    #Find the conditions with that sample
    sub_T = T[T['sample']==s]
    #Create look up dictionary of unique drugs
    to_remove = sub_T[['drug'+str(i)+'_conc' for i in range(10)]].mean()==0
    #Fit within each experiment...
    idx = [int(i.split('_')[0][-1]) for i in to_remove.index[~to_remove.values].values]
    lkup = {};
    #For each drug column
    for e in idx:
        #Find the unique drugs
        lkup['drug'+str(e)+'_unique'] = sub_T['drug'+str(e)+'_name'].unique()
        #For each drug, fit a hill equation
        for d in lkup['drug'+str(e)+'_unique']:
            if d!='none': #Don't fit if drug is none
                #Subset data
                sub_sub_T = sub_T[sub_T['drug'+str(e)+'_name']==d] 
                #Create a list of other columns not including the current drug column
                tmp_l = []
                for i in range(10):
                    if i!=e:
                        tmp_l.append('drug'+str(i)+'_conc')
                #Subset out the conditions where all other drug concentrations are zero
                sub_sub_sub_T = sub_sub_T[(sub_sub_T[tmp_l]==0).all(axis=1)]
                #Fit a hill equation (2-parameter)
                d1 = sub_sub_sub_T['drug'+str(e)+'_conc'].values
                E = sub_sub_sub_T['value'].values
                popt1, p1 , perr1 = fit_drc(d1,E,E_fx=E_fx,E_bd=E_bd)
                emx1.append(popt1[1])
# =============================================================================
# Now look at the Russ Dataset
# ============================================================================
T = pd.read_csv('../../Data/Figure5_data/russ_2018/russ_data_reformatted.csv')
# =============================================================================
# Now for each drug-sample single pair fit a hill curve to calculate the synergy
# =============================================================================
from fit_code import fit_drc,ll4,ll4_inv
#Bounds for the fitting equation
E_fix = None;E_bnd = [[.99,0.],[1.01,1.]]
E_fx = [np.nan,np.nan] if E_fix is None else E_fix; E_bd = [[-np.inf,-np.inf],[np.inf,np.inf]] if E_bnd is None else E_bnd
samples = T['sample'].unique()
#Unique samples
T['bliss'] = np.nan;  T['num_drugs'] = np.nan; T['loewe'] = np.nan
#For every sample
emx=[]
for s in samples:
    #Find the conditions with that sample
    sub_T = T[T['sample']==s]
    #Create look up dictionary of unique drugs
    lkup = {};
    #For each drug column
    for e in range(10):
        #Find the unique drugs
        lkup['drug'+str(e)+'_unique'] = sub_T['drug'+str(e)+'_name'].unique()
        #For each drug, fit a hill equation
        for d in lkup['drug'+str(e)+'_unique']:
            if d!='none': #Don't fit if drug is none
                #Subset data
                sub_sub_T = sub_T[sub_T['drug'+str(e)+'_name']==d] 
                #Create a list of other columns not including the current drug column
                tmp_l = []
                for i in range(10):
                    if i!=e:
                        tmp_l.append('drug'+str(i)+'_conc')
                #Subset out the conditions where all other drug concentrations are zero
                sub_sub_sub_T = sub_sub_T[(sub_sub_T[tmp_l]==0).all(axis=1)]
                #Fit a hill equation (2-parameter)
                d1 = sub_sub_sub_T['drug'+str(e)+'_conc'].values
                E = sub_sub_sub_T['value'].values
                popt1, p1 , perr1 = fit_drc(d1,E,E_fx=E_fx,E_bd=E_bd)
                emx.append(popt1[1])





bins=np.histogram(np.hstack((emx1,emx)), bins=10)[1] #get the bin edges

plt.figure(figsize=(2,2))
plt.hist(emx1,bins=bins)
plt.xlabel('Fit Drug Emax')
plt.ylabel('Frequency')
plt.title('Katzir et al. Emax')
xlim = plt.xlim()
plt.tight_layout()
print('Percent of drugs with Emax>0.25: ' + str(sum(np.array(emx)>.2)/float(len(emx))))
plt.savefig('katzir_emx.pdf',bbox_inches=0.)




plt.figure(figsize=(2,2))
plt.hist(emx,bins=bins)
plt.xlabel('Fit Drug Emax')
plt.ylabel('Frequency')
plt.title('Russ et al. Emax')
plt.xlim(xlim)
plt.tight_layout()
print('Percent of drugs with Emax>0.25: ' + str(sum(np.array(emx)>.2)/float(len(emx))))
plt.savefig('russ_emx.pdf',bbox_inches=0.)




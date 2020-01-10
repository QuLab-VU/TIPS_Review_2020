#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:16:48 2019

@author: meyerct6
"""


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *
import matplotlib.cm as cm
from matplotlib import rc
import glob
import numpy as np
import pandas as pd

rc('text', usetex=False)
font = {'family' : 'arial',
        'weight':'normal',
        'size'   : 8}
axes = {'linewidth': 2}
rc('font', **font)
rc('axes',**axes)

# =============================================================================
# Read in data and format
# =============================================================================
df = pd.read_excel('41564_2018_252_MOESM3_ESM.xlsx',sheet_name=None)
T = pd.DataFrame([])
for e,k in enumerate(df.keys()):
    if e!=0:
        tmp = df[k]
        drgs = list(tmp)[0:list(tmp).index('norm_gr_1')]
        for e1,v in enumerate(drgs):
            tmp['drug'+str(e1)+'_name'] = v
            tmp = tmp.rename(columns={v:'drug'+str(e1)+'_conc'})
        tmp['sample'] = k[0:2]
        T = T.append(tmp,ignore_index=True)
        
#Max number of drugs = 9    
for e in range(10):
    T.loc[T['drug'+str(e)+'_name'].isna(),'drug'+str(e)+'_name'] = 'none'
    T.loc[T['drug'+str(e)+'_conc'].isna(),'drug'+str(e)+'_conc'] = 0.0
T = T.melt(id_vars=list(T)[0:list(T).index('norm_gr_1')] + ['sample'],value_vars=['norm_gr_1','norm_gr_2'])
T.to_csv('russ_data_reformatted.csv',index=False)

# =============================================================================
# Now for each drug-sample single pair fit a hill curve to calculate the synergy
# =============================================================================
from fit_code import fit_drc,ll4,ll4_inv
#Bounds for the fitting equation
E_fix = [1.,0.];E_bnd = None
E_fx = [1.,0.] if E_fix is None else E_fix; E_bd = [[-np.inf,-np.inf],[np.inf,np.inf]] if E_bnd is None else E_bnd
samples = T['sample'].unique()
#Unique samples
T['bliss'] = np.nan;  T['num_drugs'] = np.nan; T['loewe'] = np.nan
#For every sample
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
                #Save the results in the look up table
                lkup[d+'_parms'] = popt1
                lkup[d+'_pval'] = p1
    #Now for every row caluclate Loewe and Bliss according to the fit
    for i in sub_T.index:
        bliss_val = 1; #bliss count
        loewe_val=0; #loewe count
        dcnt=0 #number of drugs count
        #For each non-zero drug concentration
        for e in range(10):
            if sub_T['drug'+str(e)+'_conc'].loc[i]!=0:
                #Bliss = U1*U2*U3...*Un
                bliss_val = bliss_val * ll4(sub_T['drug'+str(e)+'_conc'].loc[i],*lkup[sub_T['drug'+str(e)+'_name'].loc[i]+'_parms'])
                #Loewe = d1/d1' + d2/d2' + d3/d3' +.... where dx' is the concentration of dx requried to observed effect E of the combination (d1,d2,d3,...)
                loewe_val = loewe_val + (sub_T['drug'+str(e)+'_conc'].loc[i])/(ll4_inv(sub_T['value'].loc[i],*lkup[sub_T['drug'+str(e)+'_name'].loc[i]+'_parms']))
                dcnt+=1          
        if dcnt>1: #Only calculate bliss and loewe for number of drugs greater than 1.
            T.loc[i,'bliss'] = bliss_val-sub_T['value'].loc[i] #Predicted effect minus observed effect.  If predicted effect is < observed effect then antagonistic.  
            T.loc[i,'loewe'] = -np.log10(loewe_val) #if loewe_val>1 antagonistic, loewe_val<1 synergistic.
            T.loc[i,'num_drugs'] = dcnt
            
#Try to replicate Kishony/Russ analysis           
#    for i in sub_T.index:
#        bliss_val = 1;loewe_val=0;dcnt=0
#        for e in range(10):
#            if sub_T['drug'+str(e)+'_conc'].loc[i]!=0:
#                d50 = (ll4_inv(.5,*lkup[sub_T['drug'+str(e)+'_name'].loc[i]+'_parms']))
#                bliss_val = bliss_val * (1-ll4(d50,*lkup[sub_T['drug'+str(e)+'_name'].loc[i]+'_parms']))
#                loewe_val = loewe_val + (sub_T['drug'+str(e)+'_conc'].loc[i])/(d50)
#                dcnt+=1          
#        if dcnt>1:
#            T.loc[i,'bliss'] =np.log10(sub_T['value'].loc[i]/bliss_val)
#            T.loc[i,'loewe'] = np.log10(loewe_val/1.)
#            T.loc[i,'num_drugs'] = dcnt
                

T = T[T['num_drugs']>1.]
T.to_csv('russ_synergy.csv',index=False)


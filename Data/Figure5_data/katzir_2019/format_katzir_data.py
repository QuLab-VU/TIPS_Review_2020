#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 15:58:11 2019

@author: meyerct6
"""

#Format the data from Alon
import pandas as pd
import glob
import numpy as np
# cd /home/meyerct6/Desktop/higher_order_interactions/katzir_2019/journal.pcbi.1006774.s012/DataForPaper

#Recreate Tables 1 and 2:
ec_conc = pd.DataFrame({'drug':['AMP','AZI','AZT','CHL','IRG','MER','MOX','RIF','SPE','TET'],'max_conc':[8,5,.04,2.6,.9,.2,.14,7.,18.,1.]}).set_index('drug')
mt_conc = pd.DataFrame({'drug':['BDQ','CLZ','ETA','ETH','INH','LIN','MOX','PRE','RIF'],'max_conc':[.6,2.8,3,1.5,.18,3,.35,.8,.06]}).set_index('drug')

#First Build the Ecoli Pairs
df = pd.read_excel('allpairsof10Ecoli.xlsx',sheet_name=None)
key = df['drugs'][['#','abbreviation']]
rep1 = df['rep1']
rep2 = df['rep2']
for i in reversed(xrange(14)):
    rep1[i]= rep1[i]/rep1[0]
    rep2[i]= rep2[i]/rep2[0]
rep1=pd.melt(rep1,id_vars=['drug1','drug2'])
rep2=pd.melt(rep2,id_vars=['drug1','drug2'])
df = rep1.append(rep2,ignore_index=True)

for k in key.index:
    df.loc[df['drug1']==key.loc[k,'#'],'drug1']=key.loc[k,'abbreviation']
    df.loc[df['drug2']==key.loc[k,'#'],'drug2']=key.loc[k,'abbreviation']
           
df['drug1.conc'] = df['variable']
df['drug2.conc'] = df['variable']

for i in df.index:
    if df.loc[i,['drug1','drug2']].isna().any():
        df.loc[i,'drug2.conc'] = 0.
        df.loc[i,'drug1.conc']=np.linspace(0, ec_conc.loc[df.loc[i,'drug1'],'max_conc'],df['variable'].max()+1)[df.loc[i,'variable']]
    else:
        df.loc[i,'drug1.conc']=np.linspace(0, ec_conc.loc[df.loc[i,'drug1'],'max_conc'],df['variable'].max()+1)[df.loc[i,'variable']]/2.
        df.loc[i,'drug2.conc']=np.linspace(0, ec_conc.loc[df.loc[i,'drug2'],'max_conc'],df['variable'].max()+1)[df.loc[i,'variable']]/2.
    
    
df['sample'] = 'EC'
ec_key  = key
df = df.reset_index(drop=True)
#Reorganize so all drugs are in unique rows
cmat = np.zeros((len(df),10))
for i in df.index:
        for k in [1,2]:
            if isinstance(df.loc[i,'drug'+str(k)],basestring):
                idx = ec_key.loc[ec_key['abbreviation']==df.loc[i,'drug'+str(k)],'#']-1
                cmat[i,idx] = df.loc[i,'drug'+str(k)+'.conc']
                
                
mdf = pd.DataFrame(cmat,columns=['drug'+str(i)+'_conc' for i in range(10)])
for i in range(10):
    mdf['drug'+str(i)+'_name'] = ec_key.loc[i,'abbreviation']
mdf['value'] = df['value']
mdf['sample'] = 'EC'
mdf['expt'] = '2-EC'

#Next Build the Mtb Pairs
df = pd.read_excel('allpairsof10Mtb.xlsx',sheet_name=None)
key = df['drugs'][['#','abbreviation']]
rep1 = df['rep1']
rep2 = df['rep2']
for i in reversed(xrange(14)):
    rep1[i]= rep1[i]/rep1[0]
    rep2[i]= rep2[i]/rep2[0]
rep1=pd.melt(rep1,id_vars=['drug1','drug2'])
rep2=pd.melt(rep2,id_vars=['drug1','drug2'])
df = rep1.append(rep2,ignore_index=True)

df = df[(df['drug1']!=10) & (~df['drug1'].isna())]
for k in key.index:
    df.loc[df['drug1']==key.loc[k,'#'],'drug1']=key.loc[k,'abbreviation']
    df.loc[df['drug2']==key.loc[k,'#'],'drug2']=key.loc[k,'abbreviation']
           
df['drug1.conc'] = df['variable']
df['drug2.conc'] = df['variable']

for i in df.index:
    if df.loc[i,['drug1','drug2']].isna().all():
        continue
    elif df.loc[i,['drug1','drug2']].isna().any():
        df.loc[i,'drug2.conc'] = 0.
        df.loc[i,'drug1.conc']=np.linspace(0, mt_conc.loc[df.loc[i,'drug1'],'max_conc'],df['variable'].max()+1)[df.loc[i,'variable']]
    else:
        df.loc[i,'drug1.conc']=np.linspace(0, mt_conc.loc[df.loc[i,'drug1'],'max_conc'],df['variable'].max()+1)[df.loc[i,'variable']]/2.
        df.loc[i,'drug2.conc']=np.linspace(0, mt_conc.loc[df.loc[i,'drug2'],'max_conc'],df['variable'].max()+1)[df.loc[i,'variable']]/2.
    

mt_key = key
#Reorganize so all drugs are in unique rows
df = df.reset_index(drop=True)
cmat = np.zeros((len(df),10))
for i in df.index:
        for k in [1,2]:
            if isinstance(df.loc[i,'drug'+str(k)],basestring):
                idx = mt_key.loc[mt_key['abbreviation']==df.loc[i,'drug'+str(k)],'#']-1
                cmat[i,idx] = df.loc[i,'drug'+str(k)+'.conc']


tmp = pd.DataFrame(cmat,columns=['drug'+str(i)+'_conc' for i in range(10)])
for i in range(9):
    tmp['drug'+str(i)+'_name'] = mt_key.loc[i,'abbreviation']
tmp['value'] = df['value']
tmp['sample'] = 'MT'
tmp['expt'] = '2-MT'

mdf = mdf.append(tmp,ignore_index=True)
mdf = mdf.reset_index(drop=True)

#Now read in Ecoli 3 ab combinations
df = pd.read_excel('Ecoli030817.xlsx',sheet_name=None)
for k in df.keys():
    tmp = df[k].copy()
    for v in ['drugs', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']:
        tmp.loc[tmp[v]==1,v] = tmp.loc[0,v]
    for v in range(5):
        tmp.iloc[0,v] = ['drugs', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'][v]
    tmp.columns = tmp.loc[0,:]
    tmp = tmp[1:].reset_index(drop=True)
    for i in reversed(xrange(11)):
        tmp[i]= tmp[i]/tmp[0]    
    tmp = pd.melt(tmp,id_vars=['drugs', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'])  
    #zero is now the variable column!for k in key.index:
    cmat = np.zeros((len(tmp),10))
    for i in tmp.index:
        for v in range(5):
            idx = tmp.iloc[i,v]
            if idx!=0:
                cmat[i,idx-1] = np.linspace(0, ec_conc.loc[ec_key.loc[idx-1,'abbreviation'],'max_conc'],12)[int(tmp.loc[i,0])]/sum(tmp.iloc[i,0:5]!=0)
   
    
    foo = pd.DataFrame(cmat,columns=['drug'+str(i)+'_conc' for i in range(10)])
    for i in range(10):
        foo['drug'+str(i)+'_name'] = ec_key.loc[i,'abbreviation']
    foo['value'] = tmp['value']
    foo['sample'] = 'EC'
    foo['expt'] = '3-EC'
    mdf = mdf.append(foo,ignore_index=True)


#Now read in Ecoli 5 ab combinations
df = pd.read_excel('Ecoli0609results.xlsx',sheet_name=None)
for k in df.keys():
    if k!='drugs':
        tmp = df[k].copy()
        cols = list(tmp)
        for v in range(5):
            tmp.loc[tmp[cols[v]]==1,cols[v]] = cols[v]
        cols = ['drugs','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 4'] + list(range(14))
        tmp.columns = cols
        tmp = tmp.reset_index(drop=True)
        for i in reversed(xrange(14)):
            tmp[i]= tmp[i]/tmp[0]  
        tmp = pd.melt(tmp,id_vars=['drugs', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'])  
        #zero is now the variable column!for k in key.index:
        cmat = np.zeros((len(tmp),10))
        for i in tmp.index:
            for v in range(5):
                idx = tmp.iloc[i,v]
                if idx!=0:
                    cmat[i,idx-1] = np.linspace(0, ec_conc.loc[ec_key.loc[idx-1,'abbreviation'],'max_conc'],14)[int(tmp.loc[i,'variable'])]/sum(tmp.iloc[i,0:5]!=0)
       
        
        foo = pd.DataFrame(cmat,columns=['drug'+str(i)+'_conc' for i in range(10)])
        for i in range(10):
            foo['drug'+str(i)+'_name'] = ec_key.loc[i,'abbreviation']
        foo['value'] = tmp['value']
        foo['sample'] = 'EC'
        foo['expt'] = '5-EC'
        mdf = mdf.append(foo,ignore_index=True)    

df = pd.read_excel('Mtb0609results.xlsx',sheet_name=None)
for k in df.keys():
    if k!='drugs':
        tmp = df[k].copy()
        cols = list(tmp)
        for v in range(5):
            tmp.loc[tmp[cols[v]]==1,cols[v]] = cols[v]
        cols = ['drugs','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 4'] + list(range(14))
        tmp.columns = cols
        tmp = tmp.reset_index(drop=True)
        for i in reversed(xrange(14)):
            tmp[i]= tmp[i]/tmp[0]  
        tmp = pd.melt(tmp,id_vars=['drugs', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'])  
        #zero is now the variable column!for k in key.index:
        cmat = np.zeros((len(tmp),10))
        for i in tmp.index:
            for v in range(5):
                idx = tmp.iloc[i,v]
                if idx!=0:
                    cmat[i,idx-1] = np.linspace(0, mt_conc.loc[mt_key.loc[idx-1,'abbreviation'],'max_conc'],14)[int(tmp.loc[i,'variable'])]/sum(tmp.iloc[i,0:5]!=0)
       
        
        foo = pd.DataFrame(cmat,columns=['drug'+str(i)+'_conc' for i in range(10)])
        for i in range(9):
            foo['drug'+str(i)+'_name'] = mt_key.loc[i,'abbreviation']
        foo['value'] = tmp['value']
        foo['sample'] = 'MT'
        foo['expt'] = '5-MT'
        mdf = mdf.append(foo,ignore_index=True)    

#Finally the 10 combo experiment 0822
pltMap = pd.read_excel('0822platessetup.xlsx',sheet_name=None)
for r in range(3):
    df = pd.read_excel('0822rep'+str(r+1)+'.xlsx',sheet_name=None,header=None)
    for k in df.keys():
        tmp = df[k]
        for i in reversed(xrange(14)):
            tmp[i]= tmp[i]/tmp[0]  
        ptM = pltMap[k]
        cmat = np.zeros((tmp.shape[0]*tmp.shape[1],10))
        cnt = 0;
        for i in ptM.index:
            for c in ptM.columns:
                for v in range(14):
                    if not np.isnan(ptM.loc[i,c]):
                        cmat[(i-1)*14+v,int(ptM.loc[i,c]-1)] = np.linspace(0, ec_conc.loc[ec_key.loc[int(ptM.loc[i,c]-1),'abbreviation'],'max_conc'],14)[v]/sum(~ptM.loc[i].isna())
                        
 
        foo = pd.DataFrame(cmat,columns=['drug'+str(i)+'_conc' for i in range(10)])
        for i in range(10):
            foo['drug'+str(i)+'_name'] = ec_key.loc[i,'abbreviation']
        foo['value'] = tmp.values.reshape((tmp.shape[0]*tmp.shape[1],))
        foo['sample'] = 'EC'
        foo['expt'] = '10-EC' 
        mdf = mdf.append(foo,ignore_index=True)    


mdf.to_csv('katzir_data_reformatted.csv',index=False)

for e in range(10):
    mdf.loc[mdf['drug'+str(e)+'_name'].isna(),'drug'+str(e)+'_name']='none'
#Now calculate synergy
T = mdf.copy()


# =============================================================================
# Now for each drug-sample single pair fit a hill curve to calculate the synergy
# =============================================================================
from fit_code import fit_drc,ll4,ll4_inv
#Bounds for the fitting equation
E_fix = [1.,0.];E_bnd = None
E_fx = [1.,0.] if E_fix is None else E_fix; E_bd = [[-np.inf,-np.inf],[np.inf,np.inf]] if E_bnd is None else E_bnd
T['sample'] = T['sample']+'_'+T['expt']
samples = T['sample'].unique()
#Unique samples
T['bliss'] = np.nan;  T['num_drugs'] = 0; T['loewe'] = np.nan
#For every experiment
            
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
                #Save the results in the look up table
                lkup[d+'_parms'] = popt1
                lkup[d+'_pval'] = p1
    #Now for every row caluclate Loewe and Bliss according to the fit
    for i in sub_T.index:
        bliss_val = 1; #bliss count
        loewe_val=0; #loewe count
        dcnt=0 #number of drugs count
        #For each non-zero drug concentration
        for e in idx:
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
            
T = T[T['num_drugs']>1.]
T.to_csv('katzir_synergy.csv',index=False)

#Now calculate synergy based on percent AFFECT
T = mdf.copy()
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
                popt1[1] = 0.; popt1[2] = 1. #Convert to percent effect
                #Save the results in the look up table
                lkup[d+'_parms'] = popt1
                lkup[d+'_pval'] = p1
    #Now for every row caluclate Loewe and Bliss according to the fit
    for i in sub_T.index:
        bliss_val = 1; #bliss count
        loewe_val=0; #loewe count
        dcnt=0 #number of drugs count
        #For each non-zero drug concentration
        for e in idx:
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
            
T = T[T['num_drugs']>1.]
T.to_csv('katzirAFFECT_synergy.csv',index=False)



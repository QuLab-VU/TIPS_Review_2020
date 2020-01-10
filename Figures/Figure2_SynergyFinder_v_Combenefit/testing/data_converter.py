#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:02:23 2019

@author: meyerct6
"""

#Data converter

import pandas as pd
import numpy as np
import glob
from SynergyCalculator.gatherData import subset_data, subset_expt_info

df = pd.read_csv('MasterResults_mcnlls.csv')
df['pao'] = np.nan
experiments = glob.glob('data/*_0.csv') #List of experimental files
cnt = 1 
for expt in experiments:                
    #Read in the data into a pandas data frame
    data = pd.read_table(expt, delimiter=',')
    for sample in np.unique(data['sample']):
        #Subset by sample
        sub_data = data[data['sample']==sample]
        drug_combinations = sub_data[list(['drug1','drug2'])].drop_duplicates()
        #Remove the double control condition...
        drug_combinations = drug_combinations[np.logical_and(drug_combinations['drug1']!='control', drug_combinations['drug2']!='control')]
        drug_combinations = drug_combinations.reset_index()
        #For all unique drug combinations:
        for e in drug_combinations.index:
            drug1_name = drug_combinations['drug1'][e]
            drug2_name = drug_combinations['drug2'][e]
            tmp = sub_data[(sub_data['drug1']==drug1_name)&(sub_data['drug2']==drug2_name)]
            df.loc[(df['drug1_name']==drug1_name.lower())&(df['drug2_name']==drug2_name.lower())&(df['sample']==sample.upper()),'pao']=sum(tmp['effect']>100.)/float(len(tmp))
            
sample,drug1_name,drug2_name,expt = np.array(df[(df['pao']==0.)&(df['R2']>.99)][['sample','drug1_name','drug2_name','expt']])[0]
data= pd.read_table(expt,delimiter=',')
data['drug1'] = data['drug1'].str.lower()
data['drug2'] = data['drug2'].str.lower()
data['sample'] = data['sample'].str.upper()

d1,d2,dip,dip_sd = subset_data(data,drug1_name,drug2_name,sample)
drug1_units, drug2_units, expt_date = subset_expt_info(data,drug1_name,drug2_name,sample)

#Make the matrix
ud1 = np.unique(d1)
ud2 = np.unique(d2)
udip = np.nan*np.zeros(len(ud1)*len(ud2))
cnt=0
for i in range(len(ud1)):
    for j in range(len(ud1)):
        udip[cnt] = np.mean(dip[(d1==ud1[i])&(d2==ud2[j])])
        cnt+=1
DD1,DD2 = np.meshgrid(ud1,ud2)
mdip = udip.reshape(DD1.shape)

#Combenefit
data = pd.DataFrame(mdip)
data.columns = list(ud1)
data.index = list(ud2)
tmp = pd.DataFrame([{'(=Agent1)':np.nan,'Agent 1':drug1_name,'Agent 2':drug2_name,'Unit1':drug1_units,'Unit2':drug2_units,'Title':'TestData'}])
tmp = tmp[['(=Agent1)','Agent 1','Agent 2','Unit1','Unit2','Title']]
data = pd.concat([data,tmp.T])
data['(=Agent2)']=np.nan
data.to_excel('combF/'+drug1_name+'_'+drug2_name+'_'+sample+'_'+'Combenefit_fmt.xls')




#SynergyFinder
data= pd.DataFrame([])
data['ConcRow'] = DD1.reshape(len(ud1)*len(ud2),)
data['ConcCol'] = DD2.reshape(len(ud1)*len(ud2),)
data['ConcRowUnit'] = drug1_units
data['ConcColUnit'] = drug2_units
data['DrugRow'] = drug1_name
data['DrugCol'] = drug2_name
data['Response'] = mdip.reshape(len(ud1)*len(ud2),)
data['BlockID'] = 1
R,C = np.meshgrid(np.arange(1,len(ud1)+1),np.arange(1,len(ud2)+1))
data['Row'] = R.reshape(len(data),)
data['Col'] = C.reshape(len(data),)
data.to_csv('synF/'+drug1_name+'_'+drug2_name+'_'+sample+'_'+'synergyFinder_fmt.csv',index=False)



drug1_name = 'ABT-888'
drug2_name = '5-FU'
sample = 'A2058'

d1,d2,dip,dip_sd = subset_data(data,drug1_name,drug2_name,sample)
drug1_units, drug2_units, expt_date = subset_expt_info(data,drug1_name,drug2_name,sample)

df = pd.DataFrame([d1,d2,dip]).T
df.columns = ['ConcRow','ConcCol','Response']
df['DrugRow'] = drug1_name
df['DrugCol'] = drug2_name
df['ConcRowUnit'] = drug1_units
df['ConcColUnit'] = drug2_units
df['BlockID'] = range(len(df))
df['Row'] = 1
df['Col'] = 1


# =============================================================================
# After running analysis
# =============================================================================

df_comb = pd.read_csv('Analysis BLISS/data/Mean_Bliss_SYN_ANT_TestData.txt',sep='  ',header=None).T
df_synF = pd.read_csv('synergy_finder_Bliss.csv',index_col=0,header=0)
df_synF = df_synF.iloc[1:,1:]
df_synF.index = range(len(df_synF))
df_synF.columns = range(len(df_synF.T))
dip_tmp = dip/100.
df_musyc = pd.DataFrame((-dip_tmp.reshape(N+1,N+1) + np.matmul(dip_tmp[d1==0].reshape(sum(d1==0),1),dip_tmp[d2==0].reshape(1,sum(d2==0))))[1:,1:]).T*100


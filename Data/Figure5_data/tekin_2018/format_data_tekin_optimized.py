#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:49:32 2019

@author: meyerct6
"""
# =============================================================================
# Import packages
# =============================================================================
import numpy as np
import pandas as pd
import re
from tqdm import tqdm
import glob
import numpy as np
def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
#Compile the results of pdf2excel
#Conversion was done using pdf2excel in 30page increments
fils = glob.glob('pdf2excel_results/*.xlsx')
fils = np.sort(fils)
for f in fils:
    with open('compiled.txt','a') as wf:
        pd.read_excel(f).to_csv(wf,index=False,header=False,sep=' ')
#Open the compiled document
with open('compiled.txt','r') as f:
    val = f.read()
#Get out non white space
val = re.split('\s',val)
val = [x.strip('"') for x in val if x!='']
#Correct errors
val = [v if v!= '1.87085858360458TMP-14' else '1.87085858360458' for v in val]

#Code to look at the blocks of experimental data
#gblks = [e for e,x in enumerate(val) if (not is_num(x) and len(x)>3 and '+' not in x)]
#pd.DataFrame(np.diff(gblks))[0].value_counts()
#
##Find problem data
#gblks[np.where(np.diff(gblks)==124)[0][0]]
#val[7000:7236]

#Find unique drugs
un_drgs = []
for e,v in enumerate(val):
    if not is_num(v) and (len(v)==3 or '+' in v):
        un_drgs = list(set(un_drgs+list(v.split('+'))))
un_drgs = [u for u in un_drgs if len(u)==3]
#Iterate through val to build conc matrix
tot_cnt = 0;cond_cnt=0;
lkup = [];df = pd.DataFrame([])
dcmat = np.nan*np.ones((len(val),len(un_drgs)))
mat = np.nan*np.ones((len(val),))
rep_cnt = 3
for e1,v in enumerate(val):
    #If not num it is either the initial string specifying concentration or it is the condition 
    if not is_num(v): #reset the drg,conc,and lookup table
        if len(v)>3 and '+' not in v: #Labels the drug and concentration
            if (rep_cnt!=3 or rep_cnt!=4) and cond_cnt!=0: #Everytime there should be 3 or 4 replicates and no left over conditions.  Basically make sure the last block was a square.
                raise(ValueError)
            drg_l,conc_l,lkup = [],[],[];cond_cnt = 0; rep_cnt=0;
            #Append the drug name and the concentration tested
            for i in range(len(v)/4):
                drg_l.append(v[i*4:(i+1)*4-1])
                conc_l.append(int(v[(i+1)*4-1]))    
        elif len(v)==3 or '+' in v: #Which condition is tested
            lkup.append(v) #Append to look up table
        else:
            raise(ValueError)
    else:
        #For each drug in the combination iterate through the conditions tested.
        #Which drugs?
        didx = [un_drgs.index(s) for s in lkup[cond_cnt].split('+')]
        for e2,di in enumerate(didx):
            ind = drg_l.index(un_drgs[di])
            dcmat[tot_cnt,di] = conc_l[ind]
        #The measured value
        mat[tot_cnt] = float(v)
        tot_cnt+=1 #Increase the total
        cond_cnt+=1 #Count the number of conditions
        if cond_cnt==len(lkup): #If reached the length of the lookup table reset for replicate row.
            cond_cnt=0 
            rep_cnt+=1

#Shrink the matrix and make dataframe
mat = mat[0:tot_cnt]
dcmat = dcmat[0:tot_cnt,:]          
nms1=[];nms2=[];
for e in range(len(un_drgs)):
    nms1.append('drug'+str(e)+'_conc')
df = pd.concat([pd.DataFrame(mat,columns=['value']),pd.DataFrame(dcmat,columns=nms1)],axis=1)
for e,u in enumerate(un_drgs):
    df['drug'+str(e)+'_name'] = u
for e in range(len(un_drgs)):
    df.loc[df['drug'+str(e)+'_conc'].isna(),'drug'+str(e)+'_conc'] = 0.
df['sample'] = 'EC'
#Remove duplicate rows
df = df.drop_duplicates()
#Put in the concentrations used.
#Concentrations according to table conc_used_table1.xlsx
conc = pd.read_excel('conc_used_table1.xlsx')
for e,u in enumerate(un_drgs):
    for i in range(3):
        v = conc.loc[(conc['Abbreviation']==u)&(conc['Number']==i+1),'Concentration (uM)'].values[0]
        df.loc[df['drug'+str(e)+'_conc']==i+1,'drug'+str(e)+'_conc'] = v
#Save the final data frame.
df.to_csv('tekin_data_reformatted_final.csv')

T = df.copy()

# =============================================================================
# Calculate Bliss and Loewe
# =============================================================================
#        
#No need to fit as the concentrations given are equal to the IC10,5,1 
def eq(d1,d2):
    h = np.log(19./9.)/np.log(d1/d2)
    c = d2/((1/19.)**(1./h))
    return (c,h)
def hillUA(d,C,h):
    return 1./(1+(d/C)**h)
def hillinvUA(E,C,h):
    return(C*(1./E-1.)**(1./h))

conc['hill'] = np.nan
conc['ec50'] = np.nan

#For each antibiotic calculate the IC50 and the hill slope
for c in conc['Abbreviation'].unique():
    tmp = conc[conc['Abbreviation']==c]
    tmp.set_index('Number',inplace=True)
    C,h = eq(tmp.loc[1,'Concentration (uM)'],tmp.loc[2,'Concentration (uM)'])
    conc.loc[conc['Abbreviation']==c,'hill']=h
    conc.loc[conc['Abbreviation']==c,'ec50']=C
  
T['bliss'] = np.nan;  T['num_drugs'] = np.nan; T['loewe'] = np.nan
#Create look up dictionary of unique drugs
lkup = {};
#For each drug column
for e in range(8):
    #Find the unique drugs
    lkup['drug'+str(e)+'_unique'] = T['drug'+str(e)+'_name'].unique()
    d = lkup['drug'+str(e)+'_unique'][0]
    lkup[d+'_parms'] = (conc.loc[conc['Abbreviation']==d,['ec50','hill']].iloc[0].values)
    
T['value'] = T['value']/100.
#Now for every row caluclate Loewe and Bliss according to the fit
#Remove all the cases of single drug
#Remove the zero conditions and the singlet conditions
T = T[~(T[['drug'+str(e)+'_conc' for e in range(8)]]==0).all(axis=1)].reset_index(drop=True)
bliss = np.nan*np.zeros(len(T));loewe=np.nan*np.zeros(len(T));num_drugs=np.zeros(len(T))
for i in tqdm(T.index):
    bliss_val = 1; #bliss count
    loewe_val=0; #loewe count
    dcnt=0 #number of drugs count
    #For each non-zero drug concentration
    for e in range(8):
        if T['drug'+str(e)+'_conc'].loc[i]!=0:
            #Bliss = U1*U2*U3...*Un
            bliss_val = bliss_val * hillUA(T['drug'+str(e)+'_conc'].loc[i],*lkup[T['drug'+str(e)+'_name'].loc[i]+'_parms'])
            #Loewe = d1/d1' + d2/d2' + d3/d3' +.... where dx' is the concentration of dx requried to observed effect E of the combination (d1,d2,d3,...)
            loewe_val = loewe_val + (T['drug'+str(e)+'_conc'].loc[i])/(hillinvUA(T['value'].loc[i],*lkup[T['drug'+str(e)+'_name'].loc[i]+'_parms']))
            dcnt+=1          
    bliss[i] = bliss_val
    loewe[i] = loewe_val
    num_drugs[i] = dcnt
    

T['bliss'] = bliss-T['value']
T['loewe'] = -np.log10(loewe)
T['num_drugs'] = num_drugs
T = T[T['num_drugs']>1.]
T.to_csv('tekin_synergy.csv',index=False)

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 08:57:40 2019

@author: meyerct6
"""

#Calculate Bliss and Loewe for the Merck dataset
import pandas as pd
import numpy as np
from SynergyCalculator.gatherData import subset_data, subset_expt_info
from SynergyCalculator.initialFit import fit_drc,ll4,ll4_inv
import os
from tqdm import tqdm
from scipy.interpolate import interp1d
import pickle
np.random.seed(1) #For reproducibility


#Bounds for the fitting the Hill equation
E_fix = None;E_bnd = [[.99,0.,0.,0.,0.],[1.01,2.5,2.5,2.5]]
E_fx = [np.nan,np.nan,np.nan,np.nan] if E_fix is None else E_fix; 
E_bd = [[-np.inf,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf]] if E_bnd is None else E_bnd

experiments = ['merck_perVia_10-29-2018.csv'] #List of experimental files
#Lists to hold results
iden =[];bliss=[];loewe=[];hsa=[];
#For each experiment
for expt in experiments:                
    #Read in the data into a pandas data frame
    data = pd.read_table(expt, delimiter=',')
    data= pd.read_table(expt,delimiter=',')
    data['drug1'] = data['drug1'].str.lower()
    data['drug2'] = data['drug2'].str.lower()
    data['sample'] = data['sample'].str.upper()
    #For each sample in the dataset
    for sample in tqdm(np.unique(data['sample']),desc='sample loop'):
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
            #Subset out the doses and data
            d1,d2,dip,dip_sd = subset_data(data,drug1_name,drug2_name,sample)
            drug1_units, drug2_units, expt_date = subset_expt_info(data,drug1_name,drug2_name,sample)
            #Try fitting using a 4-parameter Hill equation with bounds specified above
            popt1, p1 , perr1 = fit_drc(d1[d2==0], dip[d2==0],E_fx=E_fx[0:2],E_bd=[E_bd[0][0:2],E_bd[1][0:2]])
            popt2, p2 , perr2 = fit_drc(d2[d1==0], dip[d1==0],E_fx=E_fx[0:3:2],E_bd=[E_bd[0][0:3:2],E_bd[1][0:3:2]])
            
            #Arrays to store the bliss and loewe calculations in per dose.
            bl = np.nan*np.ones(len(d1));lo=np.nan*np.ones(len(d1));hs = np.nan*np.ones(len(d1))
            
            #If fit worked use Hill fit.  Otherwise use linear interpolation.
            if np.isnan(popt1).any() and np.isnan(popt2).any():
                f1 = interp1d(d1[d2==0],dip[d2==0],kind='linear')
                f1p = interp1d(dip[d2==0],d1[d2==0],kind='linear')
                f2 = interp1d(d2[d1==0],dip[d1==0],kind='linear')
                f2p = interp1d(dip[d1==0],d2[d1==0],kind='linear')
                
            elif np.isnan(popt1).any():
                f1 = interp1d(d1[d2==0],dip[d2==0],kind='linear')
                f1p = interp1d(dip[d2==0],d1[d2==0],kind='linear')
                f2 = lambda x: ll4(x,*popt2)
                f2p = lambda e: ll4_inv(e,*popt2)
                
            elif np.isnan(popt2).any():
                f1 = lambda x: ll4(x,*popt1)
                f1p = lambda e: ll4_inv(e,*popt1)
                f2 = interp1d(d2[d1==0],dip[d1==0],kind='linear')
                f2p = interp1d(dip[d1==0],d2[d1==0],kind='linear')
                
            else:
                f1 = lambda x: ll4(x,*popt1)
                f1p = lambda e: ll4_inv(e,*popt1)
                f2 = lambda x: ll4(x,*popt2)
                f2p = lambda e: ll4_inv(e,*popt2)
            
            #Calculate Bliss and Loewe
            for v in range(len(d1)):
                    if d1[v]!=0 and d2[v]!=0:
                        bl[v] = f1(d1[v])*f2(d2[v])-dip[v]
                        hs[v] = min(f1(d1[v]),f2(d2[v]))-dip[v]
                        try:
                            lo[v] = -np.log10((d1[v]/f1p(dip[v]))+(d2[v]/f2p(dip[v])))
                        except ValueError:
                            lo[v] = np.nan
            #Save the results
            iden.append((drug1_name+'_'+drug2_name+'_'+sample).upper())
            bliss.append(np.nanmean(bl))
            loewe.append(np.nanmean(lo))
            hsa.append(np.nanmean(hs))
            


#read in labels and change for bliss loewe and hsa
pickle.dump([iden,bliss,loewe,hsa],open('syn_fits.p','wb'))

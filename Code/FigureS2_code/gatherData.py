#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:42:32 2018

@author: xnmeyer
"""
import numpy as np
def subset_data(data,drug1_name,drug2_name,sample):
    sub_data = data[data['sample']==sample]
    #control data for drug 1.  Either
    indx    = ((sub_data['drug1']==drug1_name) & (sub_data['drug2.conc']==0))  & (sub_data['drug1.conc']!=0)
    d1      = sub_data[indx]['drug1.conc'].values
    d2      = sub_data[indx]['drug2.conc'].values
    dip     = sub_data[indx]['effect'].values
    dip_95ci= sub_data[indx]['effect.95ci'].values
    
    indx    = ((sub_data['drug2']==drug1_name) & (sub_data['drug1.conc']==0))  & (sub_data['drug2.conc']!=0)
    d1      = np.concatenate([d1,sub_data[indx]['drug2.conc'].values])
    d2      = np.concatenate([d2,sub_data[indx]['drug1.conc'].values])
    dip     = np.concatenate([dip,sub_data[indx]['effect'].values])
    dip_95ci= np.concatenate([dip_95ci,sub_data[indx]['effect.95ci'].values])
    
    #control for drug 2
    indx    = ((sub_data['drug1']==drug2_name) & (sub_data['drug2.conc']==0))  & (sub_data['drug1.conc']!=0)
    d1      = np.concatenate([d1,sub_data[indx]['drug2.conc'].values])
    d2      = np.concatenate([d2,sub_data[indx]['drug1.conc'].values])
    dip     = np.concatenate([dip,sub_data[indx]['effect'].values])
    dip_95ci= np.concatenate([dip_95ci,sub_data[indx]['effect.95ci'].values])
    
    indx    = ((sub_data['drug2']==drug2_name) & (sub_data['drug1.conc']==0))  & (sub_data['drug2.conc']!=0)
    d1      = np.concatenate([d1,sub_data[indx]['drug1.conc'].values])
    d2      = np.concatenate([d2,sub_data[indx]['drug2.conc'].values])
    dip     = np.concatenate([dip,sub_data[indx]['effect'].values])
    dip_95ci= np.concatenate([dip_95ci,sub_data[indx]['effect.95ci'].values])
    
    #Combination experiment
    indx    = ((sub_data['drug1']==drug1_name) & (sub_data['drug2']==drug2_name)) & ((sub_data['drug1.conc']!=0) & (sub_data['drug2.conc']!=0)) 
    d1      = np.concatenate([d1,sub_data[indx]['drug1.conc'].values])
    d2      = np.concatenate([d2,sub_data[indx]['drug2.conc'].values])
    dip     = np.concatenate([dip,sub_data[indx]['effect'].values])
    dip_95ci= np.concatenate([dip_95ci,sub_data[indx]['effect.95ci'].values])
    
    indx    = ((sub_data['drug2']==drug1_name) & (sub_data['drug1']==drug2_name)) & ((sub_data['drug1.conc']!=0) & (sub_data['drug2.conc']!=0)) 
    d1      = np.concatenate([d1,sub_data[indx]['drug2.conc'].values])
    d2      = np.concatenate([d2,sub_data[indx]['drug1.conc'].values])
    dip     = np.concatenate([dip,sub_data[indx]['effect'].values])
    dip_95ci= np.concatenate([dip_95ci,sub_data[indx]['effect.95ci'].values])
    
    #The double control condition
    indx    = ((sub_data['drug1.conc']==0) & (sub_data['drug2.conc']==0))
    d1      = np.concatenate([d1,sub_data[indx]['drug1.conc'].values])
    d2      = np.concatenate([d2,sub_data[indx]['drug2.conc'].values])
    dip     = np.concatenate([dip,sub_data[indx]['effect'].values])
    dip_95ci= np.concatenate([dip_95ci,sub_data[indx]['effect.95ci'].values])
    
    #Set as standard deviation
    dip_sd = dip_95ci/(2*1.96)
    
    #Remove nan values
    d1      = d1[~np.isnan(dip)]
    d2      = d2[~np.isnan(dip)]
    dip_sd  = dip_sd[~np.isnan(dip)]
    dip     = dip[~np.isnan(dip)]
    
    if (dip_sd<=0).any():
        string = 'WARNING: Combination Screen: Drugs(' + drug1_name + ' ' + drug2_name + ') Sample: ' + sample + ' the effect.95ci column has a value <0!  Confidence intervals (CI) on effect MUST be positive.  If CI is unknown, assign a small finite number to all conditions.'
        print string
        dip_sd[dip_sd<=0]=min(dip_sd[dip_sd>0])
        
    return d1,d2,dip,dip_sd

def subset_expt_info(data,drug1_name,drug2_name,sample):
    sub_data = data[data['sample']==sample]
    #control data for drug 1.  Either
    indx = []
    indx.append(((sub_data['drug1']==drug1_name) & (sub_data['drug2.conc']==0))  & (sub_data['drug1.conc']!=0))    
    indx.append(((sub_data['drug2']==drug1_name) & (sub_data['drug1.conc']==0))  & (sub_data['drug2.conc']!=0))   
    #control for drug 2
    indx.append(((sub_data['drug1']==drug2_name) & (sub_data['drug2.conc']==0))  & (sub_data['drug1.conc']!=0))    
    indx.append(((sub_data['drug2']==drug2_name) & (sub_data['drug1.conc']==0))  & (sub_data['drug2.conc']!=0))    
    #Combination experiment
    indx.append(((sub_data['drug1']==drug1_name) & (sub_data['drug2']==drug2_name)) & ((sub_data['drug1.conc']!=0) & (sub_data['drug2.conc']!=0)))    
    indx.append(((sub_data['drug2']==drug1_name) & (sub_data['drug1']==drug2_name)) & ((sub_data['drug1.conc']!=0) & (sub_data['drug2.conc']!=0)))
    drug1_units=[]
    drug2_units=[]
    expt_date = []
    for i in indx:
        drug1_units.append(sub_data.loc[i,'drug1.units'].unique())
        drug2_units.append(sub_data.loc[i,'drug2.units'].unique())
        expt_date.append(sub_data.loc[i,'expt.date'].unique())
    if len(np.unique(np.concatenate(drug1_units).ravel()))>1:
        raise DataError(drug1_name+' concentration has different units.  Please scale concentrations so all units are the same')
    if len(np.unique(np.concatenate(drug2_units).ravel()))>1:
        raise DataError(drug2_name+' concentration has different units.  Please scale concentrations so all units are the same')
    drug1_units = np.unique(np.concatenate(drug1_units).ravel())[0]
    drug2_units = np.unique(np.concatenate(drug2_units).ravel())[0]
    expt_date = np.unique(np.concatenate(expt_date).ravel())
    return drug1_units,drug2_units,expt_date

class DataError(Exception):
    pass
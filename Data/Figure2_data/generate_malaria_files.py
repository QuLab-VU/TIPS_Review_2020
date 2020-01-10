#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 15:45:20 2018

@author: xnmeyer
"""

import pandas as pd
import numpy as np
import glob
import os

#Data downloaded from https://tripod.nih.gov/matrix-client/
#Block numbers 131028 (3D7,Dd2,HB3 lines),131126 (3D7,Dd2,HB3 lines),131223 (Dd2,HB3 lines)
#Stored in folder 'data'
fils = glob.glob('data/1*/')
#For all folders
for f in fils:
    #read in data
    calc = pd.read_csv(f + 'calc.csv')
    meta = pd.read_csv(f + 'metadata.csv')
    res = pd.read_csv(f + 'responses.csv')
    #Which strain?
    strain = f[-6:-3]
    for i in meta.index:
        #If the confidence interval is below .9 remove
        if float(calc[calc['BlockId']==meta['BlockId'].loc[i]]['mqcConfidence'])>.9:
            d1 = np.flipud([float(k) for k in meta['RowConcs'].loc[i].split(',')])
            d2 = np.flipud([float(k) for k in meta['ColConcs'].loc[i].split(',')])
            v = res[res['BlockId']==meta['BlockId'].loc[i]]
            d1_name = meta['RowName'].loc[i]
            d2_name = meta['ColName'].loc[i]
            d1_name = ''.join(e for e in d1_name if e.isalnum())
            d2_name = ''.join(e for e in d2_name if e.isalnum())
            d1_conc = np.zeros((len(v),))
            d2_conc = np.zeros((len(v),))
            rate = np.zeros((len(v),))
            for e,k in enumerate(v.index):
                d1_conc[e] = d1[int(-v['Row'].loc[k])]
                d2_conc[e] = d2[int(-v['Col'].loc[k])]
                rate[e] = v['Value'].loc[k]
            rate_sd = np.ones((len(v),))
            mat = np.column_stack((d1_conc,d2_conc,rate,rate_sd))
	    #Create the dataframe
            d = pd.DataFrame(mat,columns =['drug1.conc','drug2.conc','effect','effect.95ci'])
            d['drug1']=d1_name
            d['drug2']=d2_name
	    d['drug1.units']='uM'
	    d['drug2.units']='uM'
            d['expt.date']=meta['BlockId'].loc[i]
            d['sample']='plasmodium_falciparum_' + strain
            if d1_name != d2_name: #Don't save the sham experiments
                cnt = 0
                while True:
                    fnm = d1_name + '_' + d2_name + '_' + strain + '_' + str(cnt)+ '.csv'
                    if ~os.path.isfile(fnm):
                        d.to_csv(fnm,sep=',',index=False)
                        break
                    else:
                        cnt=+1
                
                

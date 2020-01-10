#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 09:34:32 2019

@author: meyerct6
"""
# =============================================================================
# Import packages
# =============================================================================
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
from gatherData import subset_data
import os
from fit_code import fit_drc,ll4,ll4_inv
from scipy.optimize import curve_fit
#single drug hill equation 4-parameter
def Edrug1D(d,E0,Em,C,h):
    return Em + (E0-Em) / (1 + (d/C)**h)
#single drug hill equation 2 parameter
def Udrug1D(d,h,C):
    return Edrug1D(d,100.,0.,C,h)

# =============================================================================
# Find examples of saturating and non saturating fits in the antimalarial datasets
# =============================================================================
#MuSyC fits to malarial dataset
sub_T = pd.read_csv('../../Data/Figure2_data/MasterResults_mcnlls.csv')
#Only consider fits which converged
sub_T = sub_T[sub_T['converge_mc_nlls']==1]
sub_T = sub_T[((sub_T['E1']>30)&(np.array([eval(i)[0] for i in sub_T['E1_ci']])>30)&(np.array([eval(i)[1] for i in sub_T['E1_ci']])<50)&(sub_T['E1_obs']<50)) |
              ((sub_T['E1']<1)&(np.array([eval(i)[1] for i in sub_T['E1_ci']])<1))]

# =============================================================================
# Figure S2A
# =============================================================================
#Read in the data and fit 2 types of hill curves to it
sub_T['save_direc'] = '../../Data/Figure2_data/'
#Take the first three and plot the data:
for i in sub_T.index:
    expt        = sub_T.loc[i,'save_direc'] + os.sep+ sub_T.loc[i,'expt']
    drug1_name  = sub_T.loc[i,'drug1_name']
    drug2_name  = sub_T.loc[i,'drug2_name']
    sample      = sub_T.loc[i,'sample']
    data        = pd.read_table(expt, delimiter=',')        
    data['drug1'] = data['drug1'].str.lower()
    data['drug2'] = data['drug2'].str.lower()
    data['sample'] = data['sample'].str.upper()
    d1,d2,dip,dip_sd = subset_data(data,drug1_name,drug2_name,sample)
    d1 = d1[d2==0]
    dip = dip[d2==0]
    popt,pcov =  curve_fit(Udrug1D,d1,dip,p0=[sub_T.loc[i,'h1'],10**sub_T.loc[i,'log_C1']])

    plt.figure(figsize=(1.5,1.5))
    d1[d1==0] = min(d1[d1!=0])/10.
    x_f = np.linspace(min(d1),max(d1),100)
    y_f = Edrug1D(x_f,sub_T.loc[i,'E0'],sub_T.loc[i,'E1'],10**sub_T.loc[i,'log_C1'],sub_T.loc[i,'h1'])
    y_p = Udrug1D(x_f,*popt)
    plt.scatter(np.log10(d1),dip,label='Data',s=2)
    plt.plot(np.log10(x_f),y_f,'r',label='4-Parameter Hill Eq.')
    plt.plot(np.log10(x_f),y_p,'k',label='2-Parameter Hill Eq.')
    
    plt.xlabel('log('+drug1_name+')')
    plt.ylabel('Effect')
    plt.tight_layout()
    plt.legend(loc='bottom left')
    plt.ylim(0.,120.)
    plt.savefig(drug1_name+'_'+sample+'_dose-response.pdf',bbox_inches=0.)


# =============================================================================
# Figure S2C
# =============================================================================
sub_T = pd.read_csv('../../Data/Figure2_data/MasterResults_mcnlls.csv')
sub_T = sub_T[sub_T['converge_mc_nlls']==1]

plt.figure(figsize=(2,2))
d = sub_T[['drug1_name','drug2_name']].values.reshape((1,len(sub_T)*2))[0]
s = sub_T[['sample','sample']].values.reshape((1,len(sub_T)*2))[0]
e = v = sub_T[['E1','E2']].values.reshape((1,len(sub_T)*2))[0]
dftmp = pd.DataFrame({'drug':d,'sample':s,'Emx':e})
t = pd.DataFrame(dftmp.groupby(by=['sample','drug']).mean())['Emx'].values
plt.hist(t,bins=50)
plt.xlabel('Fit Drug Emax')
plt.ylabel('Frequency')
plt.title('Antimalarial Drugs Emax',fontsize=8)
plt.xlim(-5,120)
plt.xticks([0,50,100])
plt.tight_layout()
plt.savefig('mott_emx.pdf',bbox_inches=0.)


# =============================================================================
# Find examples of saturating and non saturating fits in the merck datasets
# =============================================================================
sub_T = pd.read_csv('../Figure4_S5_code/MasterResults_mcnlls.csv')
sub_T = sub_T[sub_T['converge_mc_nlls']==1]
sub_T = sub_T[((sub_T['E1']>.34)&(np.array([eval(i)[0] for i in sub_T['E1_ci']])>.34)&(np.array([eval(i)[1] for i in sub_T['E1_ci']])<.39)&(sub_T['E1_obs']<.40))|
              ((sub_T['E1']<.03)&(np.array([eval(i)[1] for i in sub_T['E1_ci']])<.03))]

# =============================================================================
# Figure S2B
# =============================================================================
sub_T['save_direc'] = '../Figure4_S5_code/'
#Read in the data and fit 2 types of hill curves to it
for i in sub_T.index:
    expt        = sub_T.loc[i,'save_direc'] + os.sep+ sub_T.loc[i,'expt']
    drug1_name  = sub_T.loc[i,'drug1_name']
    drug2_name  = sub_T.loc[i,'drug2_name']
    sample      = sub_T.loc[i,'sample']
    data        = pd.read_table(expt, delimiter=',')        
    data['drug1'] = data['drug1'].str.lower()
    data['drug2'] = data['drug2'].str.lower()
    data['sample'] = data['sample'].str.upper()
    d1,d2,dip,dip_sd = subset_data(data,drug1_name,drug2_name,sample)
    d1 = d1[d2==0]
    dip = dip[d2==0]
    popt,pcov =  curve_fit(Udrug1D,d1,dip*100.,p0=[sub_T.loc[i,'h1'],10**sub_T.loc[i,'log_C1']])

    plt.figure(figsize=(1.5,1.5))
    d1[d1==0] = min(d1[d1!=0])/10.
    x_f = np.linspace(min(d1),max(d1),100)
    y_f = Edrug1D(x_f,sub_T.loc[i,'E0'],sub_T.loc[i,'E1'],10**sub_T.loc[i,'log_C1'],sub_T.loc[i,'h1'])
    y_p = Udrug1D(x_f,*popt)

    plt.scatter(np.log10(d1),dip*100.,label='Data',s=2)
    plt.plot(np.log10(x_f),y_f*100.,'r',label='4-Parameter Hill Eq.')
    plt.plot(np.log10(x_f),y_p,'k',label='2-Parameter Hill Eq.')

    plt.xlabel('log('+drug1_name+')')
    plt.ylabel('Effect')
    plt.tight_layout()
    plt.legend(loc='bottom left')
    plt.ylim(0.,120.)
    plt.savefig(drug1_name+'_'+sample+'_dose-response.pdf',bbox_inches=0.)
    
# =============================================================================
# Figure S2D
# =============================================================================
sub_T = pd.read_csv('../Figure4_S5_code/MasterResults_mcnlls.csv')
sub_T = sub_T[sub_T['converge_mc_nlls']==1]

plt.figure(figsize=(2,2))
d = sub_T[['drug1_name','drug2_name']].values.reshape((1,len(sub_T)*2))[0]
s = sub_T[['sample','sample']].values.reshape((1,len(sub_T)*2))[0]
e = v = sub_T[['E1','E2']].values.reshape((1,len(sub_T)*2))[0]*100.
dftmp = pd.DataFrame({'drug':d,'sample':s,'Emx':e})
t = pd.DataFrame(dftmp.groupby(by=['sample','drug']).mean())['Emx'].values
plt.hist(t,bins=50)

plt.xlabel('Fit Drug Emax')
plt.ylabel('Frequency')
plt.title('Anti-cancer Drugs Emax',fontsize=8)
plt.xlim(-5,120)
plt.xticks([0,50,100])
plt.tight_layout()
plt.savefig('oneil_emx.pdf',bbox_inches=0.)

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:02:23 2019

@author: meyerct6
"""
# =============================================================================
# Import packages
# =============================================================================
import pandas as pd     
import numpy as np
import os
#Figures making
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
#Functions for subsetting data
from gatherData import subset_data, subset_expt_info

# =============================================================================
# Read in data on MuSyC fits for the anti-malarial screen
# Read in synergyFinder and combenefit analysis
# Run synergyFinder using the synergy_finder.R file
# Run combenefit using according to the notes_combenefit.txt file
# =============================================================================
#Read in musyc fits
df = pd.read_csv('../../Data/Figure2_data/MasterResults_mcnlls.csv')
df['barcode'] = df['drug1_name']+'_'+df['drug2_name']+'_'+df['sample']
#Set up data frame to hold information on bliss loewe and hsa
df['mean_dif_bliss'] = np.nan;      df['mean_dif_loewe'] = np.nan;      df['mean_dif_hsa'] = np.nan
df['mean_synF_bliss'] =  np.nan;    df['mean_synF_loewe'] = np.nan;     df['mean_synF_hsa'] = np.nan
df['mean_comb_bliss'] = np.nan;     df['mean_comb_loewe'] = np.nan;     df['mean_comb_hsa'] = np.nan
df['sum_synF_bliss'] =  np.nan;     df['sum_synF_loewe'] = np.nan;     df['sum_synF_hsa'] = np.nan
df['sum_comb_bliss'] = np.nan;      df['sum_comb_loewe'] = np.nan;     df['sum_comb_hsa'] = np.nan
df['dif_mean_bliss'] = np.nan;      df['dif_mean_loewe'] = np.nan;     df['dif_mean_hsa'] = np.nan
df['dif_mean_sign_bliss'] = np.nan; df['dif_mean_sign_loewe'] = np.nan; df['dif_mean_sign_hsa'] = np.nan

#Read in the synergyfinder and combenefit analysis
for i in df.index:
    f = df['barcode'].loc[i]
    for mth in ['Bliss','Loewe','HSA']:
        coF = '../../Data/Figure2_data/combF/'+f+'/Analysis '+ mth.upper()+ '/data/Mean_'+mth+'_SYN_ANT_TestData.txt'
        syF = '../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv'
        try: #If combenefit did not converge it will not have a file.
            if os.path.isfile(syF) and os.path.isfile(coF):
                df_comb = pd.read_csv(coF,sep='  ',header=None).T 
                df_synF = pd.read_csv(syF,index_col=0,header=0)
                df_synF = df_synF.iloc[1:,1:]
                df_synF.index = range(len(df_synF))
                df_synF.columns = range(len(df_synF.T)) 
                df.loc[i,'mean_dif_'+mth.lower()] = abs(df_comb-df_synF).mean().mean()
                df.loc[i,'mean_synF_'+mth.lower()] =  df_synF.mean().mean()
                df.loc[i,'mean_comb_'+mth.lower()] =  df_comb.mean().mean()
                df.loc[i,'sum_comb_'+mth.lower()] = df_comb.max().max()
                df.loc[i,'sum_synF_'+mth.lower()] = df_synF.max().max()
                df.loc[i,'dif_mean_'+mth.lower()] = df.loc[i,'mean_comb_'+mth.lower()] - df.loc[i,'mean_synF_'+mth.lower()]
                df.loc[i,'dif_mean_sign_'+mth.lower()] = np.sign(df.loc[i,'mean_comb_'+mth.lower()]) == np.sign(df.loc[i,'mean_synF_'+mth.lower()])
        except:
            pass
        
#Look for example where the difference in bliss on the mean over the surface was high
df[((df['dif_mean_sign_bliss'])==0) & (df['R2']>.95) & (df['dif_mean_bliss']<-35)].T
#Selected example
i = 701  #HB3, emetine, nvpbgt226
f = df['barcode'].loc[i]
mth = 'Bliss'
coF = '../../Data/Figure2_data/combF/'+f+'/Analysis '+ mth.upper()+ '/data/Mean_'+mth+'_SYN_ANT_TestData.txt'
syF = '../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv'
if os.path.isfile(syF) and os.path.isfile(coF):
    df_comb = pd.read_csv('../../Data/Figure2_data/combF/'+f+'/Analysis '+ mth.upper()+ '/data/Mean_'+mth+'_SYN_ANT_TestData.txt',sep='  ',header=None).T 
    df_synF = pd.read_csv('../../Data/Figure2_data/synF/'+f+'_synergyFinder_fmt_'+mth+'.csv',index_col=0,header=0)
    df_synF = df_synF.iloc[1:,1:]
    df_synF.index = range(len(df_synF))
    df_synF.columns = range(len(df_synF.T))

data = pd.read_csv('../../Data/Figure2_data/data/Emetine_NVPBGT226_HB3_0.csv')
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

#Combenefit
data = pd.DataFrame(mdip)
data.columns = list(ud1)
data.index = list(ud2)


# =============================================================================
# Figure2 A,B
# =============================================================================
fig = plt.figure(figsize=(7,4))
ax = []
ax.append(plt.subplot2grid((10,3),(0,0),rowspan=7))
ax.append(plt.subplot2grid((10,3),(0,1),rowspan=7))
ax.append(plt.subplot2grid((10,3),(0,2),rowspan=7))
cax = []
cax.append(plt.subplot2grid((10,3),(8,0),rowspan=1))
cax.append(plt.subplot2grid((10,3),(8,1),rowspan=1))
cax.append(plt.subplot2grid((10,3),(8,2),rowspan=1))
plt.subplots_adjust(wspace=0,hspace=0.)
plt.sca(ax[0])
cmap = cm.cool_r
cmap.set_bad('white',1.)
plt.imshow(data, vmin=0,vmax=200.,origin='lower',cmap=cmap)
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

df_comb.insert(0,-1,np.nan)
tmp = df_comb.T 
tmp.insert(0,-1,np.nan)
df_comb = tmp.T

plt.sca(ax[1])
cmap = cm.seismic
cmap.set_bad('gray',1.)
plt.imshow(df_comb, vmin=-150,vmax=150.,origin='lower',cmap=cmap)
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_ylabel('',labelpad=-10)
ax[1].set_xlabel('',labelpad=-10)
ax[1].set_title('Combenefit (Bliss)\n'+'Mean:'+str(np.round(df_comb.mean().mean(),decimals=2)))
cb = plt.colorbar(cax=cax[1],orientation='horizontal')
cb.set_ticks((-100,0,100))

plt.sca(ax[2])
cmap = cm.seismic
cmap.set_bad('gray',1.)
plt.imshow(df_synF, vmin=-150,vmax=150.,origin='lower',cmap=cmap)
ax[2].set_xticks([])
ax[2].set_yticks([])
ax[2].set_ylabel('',labelpad=-10)
ax[2].set_xlabel('',labelpad=-10)
ax[2].set_title('SynergyFinder (Bliss)\n'+'Mean:'+str(np.round(df_synF.mean().mean(),decimals=2)))
cb = plt.colorbar(cax=cax[2],orientation='horizontal')
cb.set_ticks((-100,0,100))
fig.savefig('conflicting_calculations.pdf',bbox_inches=0.)

# =============================================================================
# Figure 2C
# =============================================================================
fig = plt.figure(figsize=(2,2))
ax = plt.subplot(111)
x = []
for m in ['loewe','bliss','hsa']:
    tmp = df[~df[['mean_synF_'+m,'mean_comb_'+m]].isna().any(axis=1)]
    x.append(sum((tmp['mean_synF_'+m]>0)&(tmp['mean_comb_'+m]>0))/float(len(tmp))*100)
    x.append(sum((tmp['mean_synF_'+m]<0)&(tmp['mean_comb_'+m]<0))/float(len(tmp))*100)
    x.append(100.-x[-1]-x[-2])
    
plt.bar(range(3),[x[0],x[3],x[6]],label='Synergistic')
plt.bar(range(3),[x[1],x[4],x[7]],bottom=[x[0],x[3],x[6]],label='Antagonistic')
plt.bar(range(3),[x[2],x[5],x[8]],bottom=[100-x[2],100-x[5],100-x[8]],label="Conflicting")
plt.ylim(0,100)
plt.title('Agreement between\nSynergyFinder and Combenefit',fontsize=8)
plt.ylabel('Percent')
plt.xlabel('')
plt.xticks(range(3),['Loewe','Bliss','HSA'],rotation=45)
plt.tight_layout()
ax.legend(bbox_to_anchor=(1,-.25),ncol=3,handletextpad=.1)
fig.savefig('conflicting_results.pdf',bbox_inches=0.)

# =============================================================================
# Figure 3A, S3A
# =============================================================================
fig = plt.figure(figsize=(5,2))
mth = 'loewe'
ax1 = plt.subplot2grid((2,5),(0,0),colspan=3)
ax2 = plt.subplot2grid((2,5),(1,0),colspan=3)
ax3 = plt.subplot2grid((2,5),(0,3),colspan=2,rowspan=2)
sub_df = df[['mean_comb_'+mth,'sum_comb_'+mth]]
sub_df = sub_df[~sub_df.mean(axis=1).isna()]
sub_df = sub_df.sort_values('sum_comb_'+mth)
sub_df = sub_df.reset_index(drop=True)
ax1.bar(range(len(sub_df)),sub_df['sum_comb_'+mth],edgecolor=None,alpha=.75,color='b',width=1)
ax2.bar(range(len(sub_df)),sub_df['mean_comb_'+mth],edgecolor=None,alpha=.75,color='r',width=1)
plt.sca(ax2)
plt.yscale('symlog')
plt.sca(ax3)
plt.scatter(sub_df['sum_comb_'+mth],sub_df['mean_comb_'+mth],3,c='k',alpha=.75)
plt.yscale('symlog')
plt.subplots_adjust(wspace=1,hspace=0.1)
ax1.set_xticks([])
ax2.set_xticks([])
ax1.set_xlim((0,len(sub_df)))
ax2.set_xlim((0,len(sub_df)))

ax2.set_yticks([10,0,-10,-1000])
ax3.set_yticks([10,0,-10,-1000])
ax3.set_ylabel('Max -log(Loewe)')
ax3.set_xlabel('Mean -log(Loewe)')
ax2.set_ylabel('Mean\n-log(Loewe)')
ax1.set_ylabel('Max\n-log(Loewe)')
ax1.set_title('Combenefit Summary Statistics',fontsize=8)
ax2.set_ylim((-3300,100))
ax2.set_xlabel('Anti-malarial combinations ordered by max ' + mth)

sub_df = sub_df.sort_values(by='mean_comb_loewe')
sub_sub_df = sub_df.iloc[0:14]
x = int(np.round(100*sum(sub_df['sum_comb_loewe']>sub_sub_df['sum_comb_loewe'].min())/float(len(sub_df))))
ax1.axvspan(sub_sub_df['sum_comb_loewe'].argmin(),len(sub_df),color='cyan',alpha=.3)
ax1.text(20,50,str(x))
ax2.axhspan(sub_df['mean_comb_'+mth].iloc[13],-3300,color='gold',alpha=.3)
ax2.text(20,-1000,'5')
ax3.axvspan(sub_sub_df['sum_comb_loewe'].min(),ax3.get_xlim()[1],color='cyan',alpha=.3)
ax3.axhspan(sub_df['mean_comb_'+mth].iloc[13],ax3.get_ylim()[0],color='gold',alpha=.3)
ax3.set_title('Rank Correlation: %.2f'%sub_df[['mean_comb_loewe','sum_comb_loewe']].corr('spearman').iloc[0,1],fontsize=8)
plt.tight_layout()
fig.savefig('conflicting_summStats.pdf',bbox_inches=0.)

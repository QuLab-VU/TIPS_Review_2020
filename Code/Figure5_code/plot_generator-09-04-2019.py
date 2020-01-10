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

for f in ['russ_2018','tekin_2018','katzir_2019']:
    T = pd.read_csv('../../Data/Figure5_data/'+f+'/'+f.split('_')[0]+'_synergy.csv')
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
    
    fig.savefig(f.split('_')[0]+'higherOrderTrends.pdf',bbox_inches=0.)

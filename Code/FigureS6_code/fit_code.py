#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:58:30 2019

@author: meyerct6
"""
import numpy as np
import scipy.optimize
import scipy.stats


def ll4(x, b, c, d, e):
    """
    Four parameter log-logistic function ("Hill curve")

     - b: log10(Hill slope)
     - c: Emax
     - d: E0
     - e: log10_EC50
     """
    return c+(d-c)/(1+(np.power(10,np.power(10,b)*(np.log10(x)-e))))


def ll4_inv(E,b,c,d,e):
    return np.power(10,(np.log10((d-c)/(E-c)-1)/np.power(10,b)+e))
#Fitting function
#doses = d1[d2==0]; dip_rates = dip[d2==0]; dip_std_errs=dip_sd[d2==0]
#doses = d2[d1==0]; dip_rates = dip[d1==0]; dip_std_errs=dip_sd[d1==0]
#null_rejection_threshold=0.05;E0_fix=None;Emx_fix=None;
def fit_drc(doses, dip_rates, dip_std_errs=None, 
            null_rejection_threshold=0.05,E_fx=None,E_bd=None):
    #Remove any nans
    dip_rate_nans = np.isnan(dip_rates)
    if np.any(dip_rate_nans):
        doses = doses[~dip_rate_nans]
        dip_rates = dip_rates[~dip_rate_nans]
        if dip_std_errs is not None:
            dip_std_errs = dip_std_errs[~dip_rate_nans]
            
    #Declare intial arrays
    popt = np.zeros((4,))*np.nan
    perr = np.zeros((4,))*np.nan
    
    if np.isnan(E_fx).any(): #If min/max drug effects are not fixed fit a 4 parameter hill curve
        curve_initial_guess = list(ll4_initials(doses, dip_rates))               
        if 10**curve_initial_guess[3]>max(doses): curve_initial_guess[3]=np.log10(max(doses))#If the EC50 is greater than the maximum dose
        if 10**curve_initial_guess[3]<min(doses[doses!=0]): curve_initial_guess[3]=np.log10(min(doses[doses!=0])) #If the EC50 is less than the minimum dose
                       
        hill_fn = ll4
        bounds = [(-np.inf,E_bd[0][1],E_bd[0][0],-np.inf),(np.inf,E_bd[1][1],E_bd[1][0],np.inf)]
        if curve_initial_guess[1]<E_bd[0][1]: curve_initial_guess[1]=E_bd[0][1]#If the Emx is less than the lower bound
        if curve_initial_guess[1]>E_bd[1][1]: curve_initial_guess[1]=E_bd[1][1]#If the Emx is greater than the upper bound
        if curve_initial_guess[2]<E_bd[0][0]: curve_initial_guess[2]=E_bd[0][0]#If the E0 is less than the lower bound
        if curve_initial_guess[2]>E_bd[1][0]: curve_initial_guess[2]=E_bd[1][0]#If the E0 is greater than the upper bound
                
    else: #Fit a 2 parameter hill curve (hill slope and ec50)
        curve_initial_guess = list(ll2_initials(doses,dip_rates,E_fx[0],E_fx[1]))
        if 10**curve_initial_guess[1]>max(doses): curve_initial_guess[1]=np.log10(max(doses))#If the EC50 is greater than the maximum dose
        if 10**curve_initial_guess[1]<min(doses): curve_initial_guess[1]=np.log10(min(doses[doses!=0])) #If the EC50 is less than the minimum dose
                   
        hill_fn = lambda x,b,e: ll4(x, b, E_fx[1], E_fx[0], e)     
        bounds = [(-np.inf,-np.inf),(np.inf,np.inf)]
        
#    print bounds
#    print curve_initial_guess
    try:
        popt, pcov = scipy.optimize.curve_fit(hill_fn,
                                              doses,
                                              dip_rates,
                                              p0=curve_initial_guess,
                                              sigma=dip_std_errs,
                                              maxfev=100000,
                                              bounds=bounds,
                                              )
        #Calculate uncertainty
        if np.isnan(E_fx).any():
            perr = np.sqrt(np.diag(pcov)) if not np.isnan(pcov).any() else np.zeros((4,)) * np.NAN
        else:
            if np.isnan(pcov).any():
                perr = np.zeros((4,))*np.NAN
            else:
                perr = np.sqrt(np.diag(pcov)) 
                perr = [perr[0],0.,0.,perr[1]]
            popt = [popt[0],E_fx[1],E_fx[0],popt[1]]   
 
    except RuntimeError:
        pass
        
    p = 1#p-value
    #Calculate the pvalue
    if not np.isnan(popt).any():
        # DIP rate fit
        dip_rate_fit_curve = ll4(doses, *popt)
        # F test vs flat linear "no effect" fit
        ssq_model = ((dip_rate_fit_curve - dip_rates) ** 2).sum()
        ssq_null = ((np.mean(dip_rates) - dip_rates) ** 2).sum()
        if np.isnan(E_fx).any():
            df = len(doses) - 4
        else:
            df = len(doses)-2
        f_ratio = (ssq_null-ssq_model)/(ssq_model/df)
        p = 1 - scipy.stats.f.cdf(f_ratio, 1, df)
        if p > null_rejection_threshold:
            popt = np.zeros((4,))*np.nan
            perr = np.zeros((4,))*np.nan
    else:
        popt = np.zeros((4,))*np.nan
        perr =  np.zeros((4,))*np.nan
    
    return popt, p, perr

#####To look at fit
#import matplotlib.pyplot as plt
#plt.figure()
#d = doses.copy()
#d[d==0]=min(d[d!=0])/10
#plt.scatter(np.log10(d),dip_rates)
#plt.plot(np.log10(d),hill_fn(doses,*curve_initial_guess))
#plt.scatter(np.log10(d),hill_fn(d,*popt))

# Functions for finding initial parameter estimates for curve fitting
def ll4_initials(x, y):
    c_val, d_val = _find_cd_ll4(y,x)
    b_val, e_val = _find_be_ll4(x, y, c_val, d_val)
    return b_val, c_val, d_val, e_val
def ll2_initials(x, y,E0_fix,Emx_fix):
    b_val, e_val = _find_be_ll4(x, y, Emx_fix, E0_fix)
    return b_val, e_val

def _response_transform(y, c_val, d_val):
    return np.log10((d_val-c_val)/(y-c_val)-1)


def _find_be_ll4(d, dip_rates, c_val, d_val, slope_scaling_factor=1.):
    x = d.copy()
    y = dip_rates.copy()
    x[x==0]=min(x[x!=0])/100. #Approximate zero dose
    y[y>c_val]=c_val  #Fix effects out side of max and min bounds
    y[y<d_val]=d_val
    #Transform the dose response curve to a line
    y = _response_transform(y,c_val,d_val)
    tmp = x.copy()
    x = np.log10((x[(~np.isnan(y)) & (~np.isinf(y))]))
    y = y[(~np.isnan(y)) & (~np.isinf(y))]
    if len(x)>2:
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
        b_val = np.log10(slope_scaling_factor * slope)
        e_val = -intercept
        if np.isnan(e_val) or np.isinf(e_val):
            e_val = np.min(x)+2
        if np.isnan(b_val) or np.isinf(b_val):
            b_val = 0.
    else:
        b_val = 0.
        e_val = np.mean(np.log10(tmp))
    return b_val, e_val


def _find_cd_ll4(y,x, scale=0.):
    e0 = np.mean(y[x==min(x)])
    emx = np.mean(y[x==max(x)])
    return emx, e0

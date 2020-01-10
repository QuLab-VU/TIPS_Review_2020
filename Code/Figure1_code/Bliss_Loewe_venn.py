#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:40:59 2019
@author: meyerct6
"""
# =============================================================================
# Import packages
# =============================================================================
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
# =============================================================================
# Plot Venn Diagrams
# =============================================================================
#Based on google scholar search  01.09.2020
#Subsets:
#1) MSP    drug synergy bliss OR "multiplicative survival principle" OR "fractional product method" -"dose equivalence principle" -isobologram -loewe -"combination index" -Chou -Talalay -isobole
#2) DEP    drug synergy "dose equivalence principle" OR isobologram OR loewe OR "combination index" OR Chou OR Talalay OR isobole -bliss -"multiplicative survival principle" -"fractional product method" 
#3) Both   drug synergy AND ("dose equivalence principle" OR isobologram OR loewe OR "combination index" OR Chou OR Talalay) AND (bliss OR "multiplicative survival principle" OR "fractional product method")
#4) All    drug synergy
plt.figure()
venn2(subsets = (9750,20400,2180), set_labels=('MSP','DEP'))
#All == 175,000
plt.savefig("bliss-loewe_venn.pdf")
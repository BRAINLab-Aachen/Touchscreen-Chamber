#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:55:48 2019

@author: root
"""

import numpy as np
import matplotlib.pylab as plt
import glob
import pandas as pd
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest
import os

plt.rcParams["font.family"] = "Arial"
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False


mouse_id='1218'
path=os.path.abspath(os.getcwd()+'/'+str(mouse_id)+'/*.csv')
mice_list=glob.glob(path)

trials=np.zeros((len(mice_list),1))
performance=np.zeros((len(mice_list),1))
p_val=np.zeros((len(mice_list),1))

for i in range(len(mice_list)):

    all_data=pd.read_csv(mice_list[i],delimiter=',')
    trials[i]=len(all_data)
    correct=all_data['correct']
    performance[i]=np.sum(correct)/len(correct)
    stat,p_val[i]=proportions_ztest(performance[i]*trials[i], trials[i], 0.5, alternative='larger')

plt.figure(dpi=300)    
plt.plot(performance,"r-")
plt.ylabel('Performance[%]', fontsize=14)
plt.xlabel('Session', fontsize=14)
sns.despine()




    



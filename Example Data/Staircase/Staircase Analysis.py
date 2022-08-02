#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 09:21:48 2019

@author: christopherwiesbrock
"""

import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import scipy.stats as stats
import glob
from scipy.signal import argrelextrema
import pandas as pd

path=r'H:\Backup C\Users\Chris\Desktop\Mac Up\Daten sortiert\Staircase\293/*.csv'
mice_list=glob.glob(path)
mice_list=np.sort(mice_list)
threshold=np.zeros((len(mice_list),1))
delay=np.zeros((len(mice_list),1))

for i in range(len(mice_list)):
    

    all_data=pd.read_csv(mice_list[i],delimiter=',')

    orientations=all_data['Difference']
    orientations=orientations.astype(float)
    orientations=np.abs(orientations)
    orientations=np.array(orientations)
    delay=all_data['touch_delay']
    delay=delay.astype(float)
    delay=delay[delay>5]
    delay[i]=np.mean(delay)
    local_max=argrelextrema(orientations,np.greater)
    local_min=argrelextrema(orientations, np.less)
    
    
    threshold[i]=(np.mean(orientations[local_max])+np.mean(orientations[local_min]))/2

plt.figure(dpi=300)    
plt.plot(threshold)
plt.ylabel('Orientation threshold [degree]')
plt.xlabel('Session')










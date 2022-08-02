# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:16:20 2022

@author: Chris
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 19:10:32 2021

@author: Chris Wiesbrock
"""

import numpy as np
import matplotlib.pylab as plt
import glob
import pandas as pd
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False


mouse_id='all'
path=r'H:\Backup C\Users\Chris\Desktop\Mac Up\Daten sortiert\Pal\1218/*.csv'
mice_list=glob.glob(path)
mice_list=np.sort(mice_list)
names=((len(mice_list),1))
perf_45=np.zeros((len(mice_list),1))
perf_90=np.zeros((len(mice_list),1))


for i in range(len(mice_list)):
    all_data=pd.read_csv(mice_list[i],delimiter=',')
    correct=all_data['correct']
    correct=correct.astype(float)
    orientations=all_data['orientation']
    perf_45[i]=np.sum(correct[orientations==45])/len(correct[orientations==45])
    perf_90[i]=np.sum(correct[orientations==90])/len(correct[orientations==90])
    
perf_45=perf_45*100
perf_90=perf_90*100
    
plt.figure(dpi=300)
plt.plot(perf_45, color='darkgrey')
plt.plot(perf_90, color='lightcoral')
sns.despine()
plt.xlabel('Session')
plt.ylabel('Performance [%]')


    
    









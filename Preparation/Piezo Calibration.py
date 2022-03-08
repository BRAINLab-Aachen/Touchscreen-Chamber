from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import glob
import UniversalLibrary as UL
import matplotlib.pylab as plt

import time


def lick_detection(SIDE):
    EngUnits=0
    DataValue=0
    if SIDE==0:
        
        while ((EngUnits)*(EngUnits))**0.5<1.55:
            DataValue = UL.cbAIn(0, SIDE, UL.BIP5VOLTS)
            EngUnits = UL.cbToEngUnits(0, UL.BIP5VOLTS, DataValue)
            print ((EngUnits)*(EngUnits))**0.5
          
        else: 

            get_reward(UL.FIRSTPORTA)
           
          
a=np.zeros((1000,1))
i=0
for i in range(1000):
    DataValue = UL.cbAIn(0, 0, UL.BIP5VOLTS)
    EngUnits = UL.cbToEngUnits(0, UL.BIP5VOLTS, DataValue)
    a[i]=EngUnits
    i=i+1

b=np.linspace(0,999,1000)
print 'mean ',np.mean(a)
print 'max ',np.max(a)
print 'min ',np.min(a)
plt.plot(b,a)
plt.show()
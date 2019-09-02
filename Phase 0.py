from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import UniversalLibrary as UL
import time
import matplotlib.pyplot as plt
import numpy as np

name='CW04'
date='140717'

thisExp = data.ExperimentHandler(runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=name+date)


def lick_detection(SIDE):
    EngUnits=0
    DataValue=0
    if SIDE==0:
        
        #threshold
        while ((EngUnits)*(EngUnits))**0.5<1.25:
            DataValue = UL.cbAIn(0, SIDE, UL.BIP5VOLTS)
            EngUnits = UL.cbToEngUnits(0, UL.BIP5VOLTS, DataValue)
            #print 1/(((EngUnits+1)*(EngUnits))**0.5)
          
        else: 
            print EngUnits+1
            print core.Clock()
            get_reward(UL.FIRSTPORTA)


def get_reward(PORTNUM):
    print 'reward'
    BoardNum = 0
    PortNum = PORTNUM
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort (BoardNum, PortNum, Direction)
    DataValue = 1
    UL.cbDOut(BoardNum, PortNum, DataValue)
    #sound_1 = sound.SoundPyo(value='C', secs=0.5, octave=4, stereo=True, volume=1.0, loops=0, sampleRate=44100, bits=16, hamming=True, start=0, stop=-1, name='', autoLog=True)
    #sound_1.play() 
    time.sleep(.1) #time
    BoardNum = 0
    PortNum = PORTNUM
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort (BoardNum, PortNum, Direction)
    DataValue = 0
    UL.cbDOut(BoardNum, PortNum, DataValue)

def led_on():
    BoardNum = 0
    PortNum = UL.FIRSTPORTB
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort (BoardNum, PortNum, Direction)
    DataValue = 1
    UL.cbDOut(BoardNum, PortNum, DataValue)

def led_off():
    BoardNum = 0
    PortNum = UL.FIRSTPORTB
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort (BoardNum, PortNum, Direction)
    DataValue = 0
    UL.cbDOut(BoardNum, PortNum, DataValue)

#trials
i=100
n=0
times=np.zeros((i+1,i))
#num=range(i+1)
trialclock=core.Clock()
for n in range(i):
    n=n+1
    led_on()
    lick_detection(0)
    print n
    times=float(trialclock.getTime())
    led_off()
    time.sleep(5)
    thisExp.addData('times',times)
    thisExp.nextEntry()


#thisExp.addData('times',times)
#thisExp.nextEntry()
#np.savetxt('C:\Dokumente und Einstellungen\Michael\Desktopname\Daten\\'+name+date+'.csv', times, delimiter=',')
#print num
#plt.plot(num,times,'r-')
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.04), Jul48
i 17, 2017, at 10:17
If you publish work using this script pl
ease cite the relevant PsychoPy publications
      Peirce, JW (2007) PsychoPy - Psycho
"""
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is avail84able, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

import sys # to get file system encoding
import UniversalLibrary as UL
import time

# Ensure that relative paths start from the same directory as this script6
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)
timepoint=0
n=0

def lick_detection(SIDE):
    EngUnits=0
    DataValue=0
    time.sleep(1.4)
    if SIDE==0:
        
        while ((EngUnits)*(EngUnits))**0.5<1.35:
            DataValue = UL.cbAIn(0, SIDE, UL.BIP5VOLTS)
            EngUnits = UL.cbToEngUnits(0, UL.BIP5VOLTS, DataValue)
            #print EngUnit
          
        else: 
            print EngUnits
            print core.Clock()
            get_reward(UL.FIRSTPORTA)


def get_reward(PORTNUM):
    
    
    BoardNum = 0
    PortNum = PORTNUM
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort (BoardNum, PortNum, Direction)
    DataValue = 1
    UL.cbDOut(BoardNum, PortNum, DataValue) 
    
    
    time.sleep(.15)
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
    sound_1 = sound.SoundPyo(value='C', secs=0.5, octave=4, stereo=True, volume=1.0, loops=0, sampleRate=44100, bits=16, hamming=True, start=0, stop=-1, name='', autoLog=True)
    sound_1.play()

def led_off():
    BoardNum = 0
    PortNum = UL.FIRSTPORTB
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort (BoardNum, PortNum, Direction)
    DataValue = 0
    UL.cbDOut(BoardNum, PortNum, DataValue)

# Store info about the experiment session
expName = u'Phase_1'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1280, 768), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
grating = visual.GratingStim(win=win, name='grating',
    tex=u'sin', mask=None,
    ori=0, pos=[0, 0], size=[2, 2], sf=3, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-1.0)
mouse = event.Mouse(win=win)
x, y = [None, None]

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=20, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    mouse.setPos((0,0))
    #grating.setOri(np.random.randint(0,360,1))

    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(ISI)
    trialComponents.append(grating)
    trialComponents.append(mouse)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        mouse.setPos((0,0))
        info_mouse=sum(mouse.getPos())
        t = trialClock.getTime()
        #grating.setPhase(t*2)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *grating* updates
        if t >= 0.0 and grating.status == NOT_STARTED and info_mouse==0:
            grating.setAutoDraw(True)
            mouse.setPos((0,0))
            # keep track of start time/frame for later
            grating.tStart = t  # underestimates by a little under one frame
            grating.frameNStart = frameN  # exact frame index
            
        if grating.status==STARTED and info_mouse!=0:
            
                #grating.setAutoDraw(False)
            led_on()
            lick_detection(0)
            led_off()
            timepoint=t
            n=n+1
            print n
            continueRoutine = False
            #time.sleep(0.1)
            #mouse.setPos((0,0))

        # *mouse* updates
        if t >= 0.0 and mouse.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse.tStart = t  # underestimates by a little under one frame
            mouse.frameNStart = frameN  # exact frame index
            mouse.status = STARTED
            event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
        if mouse.status == STARTED:  # only update if started and not stopped!
            buttons = mouse.getPressed()
            if sum(buttons) > 0:  # ie if any button is pressed
                # abort routine on response
                continueRoutine = False
        # *ISI* period
        if t >= 0.0 and ISI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ISI.tStart = t  # underestimates by a little under one frame
            ISI.frameNStart = frameN  # exact frame index
            ISI.start(0.5)
        elif ISI.status == STARTED: #one frame should pass before updating params and completing
            ISI.complete() #finish the static period
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials (TrialHandler)
    x, y = mouse.getPos()
    buttons = mouse.getPressed()
    trials.addData('mouse.x', x)
    trials.addData('mouse.y', y)
    trials.addData('mouse.leftButton', buttons[0])
    trials.addData('mouse.midButton', buttons[1])
    trials.addData('mouse.rightButton', buttons[2])
    trials.addData('time', timepoint)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 30 repeats of 'trials'

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort() # or data files will save again on exit
win.close()
core.quit()

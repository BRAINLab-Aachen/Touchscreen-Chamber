 #!/usr/bin/env python2
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import glob
import UniversalLibrary as UL

import time

def lick_detection(SIDE):
    EngUnits=0
    DataValue=0
    if SIDE==0:
        
        while ((EngUnits)*(EngUnits))**0.5<1.26:
            DataValue = UL.cbAIn(0, SIDE, UL.BIP5VOLTS)
            EngUnits = UL.cbToEngUnits(0, UL.BIP5VOLTS, DataValue)
        
          
        else: 

            get_reward(UL.FIRSTPORTA)
            
            
def lick_detection_no_reward(SIDE):
    EngUnits=0
    DataValue=0
    if SIDE==0:
        
        while ((EngUnits)*(EngUnits))**0.5<1.25:
            DataValue = UL.cbAIn(0, SIDE, UL.BIP5VOLTS)
            EngUnits = UL.cbToEngUnits(0, UL.BIP5VOLTS, DataValue)
            
          
        else: 
            
            print 'nope'
            #get_no_reward(UL.FIRSTPORTA)

def get_reward(PORTNUM):
    BoardNum = 0
    PortNum = PORTNUM
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort (BoardNum, PortNum, Direction)
    DataValue = 1
    UL.cbDOut(BoardNum, PortNum, DataValue)
    time.sleep(.07)
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

REPEATS=100
sound_1 = sound.Sound(value='d', secs=0.5, octave=8, stereo=True, volume=0.5, loops=0, sampleRate=44100, bits=16, hamming=True, start=0, stop=-1, name='', autoLog=True)
sound_2 = sound.Sound(value='c', secs=0.2, octave=4, stereo=True, volume=0.5, loops=0, sampleRate=44100, bits=16, hamming=True, start=0, stop=-1, name='', autoLog=True)

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'untitled.py'
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
 
expInfo['expName'] = expName
#imagedir=_thisDir+'\Stim1'
#imagedir=_thisDir+'\Stim2'
#imagedir=_thisDir+'\Stim3'
#imagedir=_thisDir+'\Stim5'
#image_list=glob.glob(imagedir+'\*.png')
image_list=(0.38,0.38,0.38)
#print image_list
trialnumber=0
bias=np.zeros((REPEATS,4))
#print len(bias)
last_choice=''
left=0
right=0
same=0
opposite=0
correct_trials=np.zeros((REPEATS,1))
reactiontime=np.zeros((REPEATS,1))
correctstim=''
orientation_difference=0
orientation=0
correct_trial=0
save_reactiontime=0
save_correct=0
save_difference=0
save_orientation=0
correct_orientation=0
orientation_range=1
orientation_diff_list=[90]
touch_delay=0
lick_delay=0
correct_output=0
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

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
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    )
win.mouseVisibile=False
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
'''
image = visual.ImageStim(win=win, name='image',
    image=None, mask='circle',
    ori=0, pos=[-5, 0], units='cm', size=[7, 7],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
image_2 = visual.ImageStim(win=win, name='image_2',
    image=None, mask='circle',
    ori=0, pos=[5, 0], units='cm', size=[7, 7],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
'''
image = visual.GratingStim(win=win, name='grating',
    tex=u'sin', mask='circle',
    ori=90, pos=[-10, 1], units='cm', size=[15, 15], sf=0.15, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-1.0)
image_2 = visual.GratingStim(win=win, name='grating',
    tex=u'sin', mask='circle',
    ori=0, pos=[10, 1], units='cm', size=[15, 15], sf=0.15, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-1.0)


mouse = event.Mouse(win=win, visible=False)
x, y = [None, None]
cross = visual.ShapeStim(win=win, name='cross', units='cm',
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
    lineWidth=3,
    closeShape=False,
    lineColor='white'
)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=REPEATS, method='random', 
    extraInfo=expInfo, originPath=None,
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
    routineTimer.add(121.000000)
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(ISI)
    trialComponents.append(cross)
    trialComponents.append(image)
    trialComponents.append(image_2)
    trialComponents.append(mouse)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
            
    chosen_image=np.random.randint(0, high=len(image_list))
    image.setSF(image_list[chosen_image])
    image_2.setSF(image_list[chosen_image])
    #image.setImage(image_list[chosen_image])
    #image_2.setImage(image_list[chosen_image])
    trialnumber=trialnumber+1
    orientation_list=[90]
    orientation_list=(orientation_list)
    mouse.setPos((0,0))
    
    
    #bias correction
    
    
    if trialnumber<10:
        if np.random.uniform(0,high=100)<=50:
            orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
            image.setOri(orientation)
            orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
            correct_orientation=int(orientation+orientation_difference)
            image_2.setOri(correct_orientation)
            correctstim='right'
            
            
        if np.random.uniform(0,high=100)>50:
            orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
            image_2.setOri(orientation)
            orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
            correct_orientation=int(orientation+orientation_difference)
            image.setOri(correct_orientation)
            correctstim='left'
            
    
    if trialnumber>11:
        bias_left=np.abs(left)
        bias_right=np.abs(right)
        bias_same=np.abs(same)
        bias_opposite=np.abs(opposite)
        if np.abs(bias_left-bias_right)==np.abs(bias_same-bias_opposite):
            if np.random.uniform(0,high=100)<=50:
                orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
                image.setOri(orientation)
                orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                correct_orientation=int(orientation+orientation_difference)
                image_2.setOri(correct_orientation)
                correctstim='right'
                
            
            if np.random.uniform(0,high=100)>50:
                orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
                image_2.setOri(orientation)
                orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                correct_orientation=int(orientation+orientation_difference)
                image.setOri(correct_orientation)
                correctstim='left'
               
                
        if np.abs(bias_left-bias_right)>np.abs(bias_same-bias_opposite):
            if bias_left>bias_right:
                orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
                image.setOri(orientation)
                orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                correct_orientation=int(orientation+orientation_difference)
                image_2.setOri(correct_orientation)
                correctstim='right'
                
            if bias_left<bias_right:
                orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
                image_2.setOri(orientation)
                orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                correct_orientation=int(orientation+orientation_difference)
                image.setOri(correct_orientation)
                correctstim='left'
                
                
        if np.abs(bias_left-bias_right)<np.abs(bias_same-bias_opposite):
            if bias_same<bias_opposite:
                if last_choice=='left':
                    orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
                    image_2.setOri(orientation)
                    orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                    correct_orientation=int(orientation+orientation_difference)
                    image.setOri(correct_orientation)
                    correctstim='left'
                    
                if last_choice=='right':
                    orientation=orientation_list[np.random.randint(0,high=len(orientation_list),size=1)]
                    image.setOri(orientation)
                    orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                    correct_orientation=int(orientation+orientation_difference)
                    image_2.setOri(correct_orientation)
                    correctstim='right'
                   
            if bias_same>bias_opposite:
                if last_choice=='left':
                    orientation=int(orientation_list[np.random.randint(0,high=len(orientation_list),size=1)])
                    image.setOri(orientation)
                    orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                    correct_orientation=int(orientation+orientation_difference)
                    image_2.setOri(correct_orientation)
                    correctstim='right'
                if last_choice=='right':
                    orientation=int(orientation_list[np.random.randint(0,high=len(orientation_list),size=1)])
                    image_2.setOri(orientation)
                    orientation_difference=orientation_diff_list[np.random.randint(0,high=orientation_range,size=1)]
                    correct_orientation=int(orientation+orientation_difference)
                    image.setOri(correct_orientation)
                    correctstim='left'
    
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        mouse.setPos((0,0))
        mouse_info=mouse.getPos()[0]
        #image.setPhase(t*2)
        #image_2.setPhase(t*2)
        if t>120:
            print 'timeout'
            core.quit()
        #print mouse_info
        # update/draw components on each frame
        if mouse_info>0:
            bias[trialnumber-1,0]=1 #colloumnds in bias array: 0=left, 1=right, 2=same. 3=opposite
            bias[trialnumber-1,1]=0
            last_choice='left'
        if mouse_info<0:
            bias[trialnumber-1,0]=0
            bias[trialnumber-1,1]=1
            last_choice='right'
            
        # *cross* updates
        if t >= 0.5 and cross.status == NOT_STARTED:
            # keep track of start time/frame for later
            cross.tStart = t  # underestimates by a little under one framef
            cross.frameNStart = frameN  # exact frame index
            cross.setAutoDraw(True)
        if cross.status == STARTED and t >= (0.5 + (0.5-win.monitorFramePeriod*0.75)): #most of one frame period left
            cross.setAutoDraw(False)
        # *ISI* period
        if t >= 0.0 and ISI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ISI.tStart = t  # underestimates by a little under one frame
            ISI.frameNStart = frameN  # exact frame index
            ISI.start(0.5)
        elif ISI.status == STARTED: #one frame should pass before updating params and completing
            ISI.complete() #finish the static period
        # *image* updates
        if t >= 1.2 and image.status == NOT_STARTED:
            # keep track of start time/frame for later
            image.tStart = t  # underestimates by a little under one frame
            image.frameNStart = frameN  # exact frame index
            image.setAutoDraw(True)
        if image.status == STARTED and mouse_info!=0: #most of one frame period left
            image.setAutoDraw(False)
            if mouse_info>0:
                last_choice=='left'
                reactiontime[trialnumber-1]=0
                save_reactiontime=0
                if correctstim=='left' and trialnumber>0:
                    touch_delay=trialClock.getTime()
                    correct_trials[trialnumber-1]=1.
                    correct_trial=1.
                    sound_2.play()
                    time.sleep(0.4)
                    led_on()
                    lick_detection(0)
                    lick_detection(0)
                    lick_detection(0)
                    led_off()
                    lick_delay=trialClock.getTime()
                    mouse.setPos((0,0))
                    
                if correctstim=='right' and trialnumber>0:
                    correct_trial=0.
                    touch_delay=trialClock.getTime()
                    win.color=[1,1,1]
                    win.flip()
                    sound_1 = sound.Sound(value='d', secs=0.5, octave=8, stereo=True, volume=0.5, loops=0, sampleRate=44100, bits=16, hamming=True, start=0, stop=-1, name='', autoLog=True)
                    sound_1.play()
                    time.sleep(0.2)
                    win.color=[0,0,0]
                    mouse.setPos((0,0))
                    image_2.setAutoDraw(False)
                    image.setAutoDraw(False)
                    mouse.setPos((0,0))
                    image.setAutoDraw(False)
                    image_2.setAutoDraw(False)
                    win.flip()
                    lick_detection_no_reward(0)
                    lick_delay=trialClock.getTime()
                    mouse.setPos((0,0))

        # *image_2* updates
        if t >= 1.2 and image_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            image_2.tStart = t  # underestimates by a little under one frame
            image_2.frameNStart = frameN  # exact frame index
            image_2.setAutoDraw(True)
        if image_2.status == STARTED and mouse_info!=0.: #most of one frame period left
            image_2.setAutoDraw(False)
            if mouse_info<0:
                last_choice=='right'
                reactiontime[trialnumber-1]=0
                save_reactiontime=0
                if correctstim=='right' and trialnumber>0:
                    touch_delay=trialClock.getTime()
                    correct_trials[trialnumber-1]=1.
                    correct_trial=1
                    sound_2.play()
                    time.sleep(0.4)
                    led_on()
                    lick_detection(0)
                    lick_detection(0)
                    lick_detection(0)
                    led_off()
                    lick_delay=trialClock.getTime()
                    mouse.setPos((0,0))
                    
                if correctstim=='left' and trialnumber>0:
                    correct_trial=0.
                    touch_delay=trialClock.getTime()
                    win.color=[1,1,1]
                    win.flip()
                    sound_1 = sound.Sound(value='d', secs=0.5, octave=8, stereo=True, volume=0.5, loops=0, sampleRate=44100, bits=16, hamming=True, start=0, stop=-1, name='', autoLog=True)
                    sound_1.play()
                    time.sleep(0.2)
                    win.color=[0,0,0]
                    mouse.setPos((0,0))
                    image_2.setAutoDraw(False)
                    image.setAutoDraw(False)
                    mouse.setPos((0,0))
                    image.setAutoDraw(False)
                    image_2.setAutoDraw(False)
                    win.flip()
                    lick_detection_no_reward(0)
                    lick_delay=trialClock.getTime()
                    mouse.setPos((0,0))
                    
        save_orientation=int(orientation)
        save_correct=int(correct_trial)
        save_difference=int(np.abs(correct_orientation-orientation))
        save_reactiontime=float(save_reactiontime)
           
        # *mouse* updates
        if t >= 0.0 and mouse.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse.tStart = t  # underestimates by a little under one frame
            mouse.frameNStart = frameN  # exact frame index
            mouse.status = STARTED
            mouse.setPos((0,0))
            event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
        if mouse.status == STARTED and mouse_info!=0: #most of one frame period left
            mouse.status = STOPPED
        #if mouse.status == STARTED:  # only update if started and not stopped!
        #    buttons = mouse.getPressed()
        #    if sum(buttons) > 0:  # ie if any button is pressed
                # abort routine on response
        #        continueRoutine = False
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
    if bias[trialnumber-1,0]+bias[trialnumber-2,0]==2:
        bias[trialnumber-1,2]=1
    if bias[trialnumber-1,0]+bias[trialnumber-2,0]==1:
        bias[trialnumber-1,3]=1
    if bias[trialnumber-1,1]+bias[trialnumber-2,1]==2:
        bias[trialnumber-1,2]=1
    if bias[trialnumber-1,1]+bias[trialnumber-2,1]==1:
        bias[trialnumber-1,3]=1
    
    if trialnumber>10:
        left=np.sum(bias[trialnumber-11:trialnumber-1,0])
        right=np.sum(bias[trialnumber-11:trialnumber-1,1])
        same=np.sum(bias[trialnumber-11:trialnumber-1,2])
        opposite=np.sum(bias[trialnumber-11:trialnumber-1,3])
    
    correct_output=correct_output+correct_trial
    print correct_output/trialnumber
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials (TrialHandler)
    trials.addData('imagename', image_list[chosen_image])
    trials.addData('correct',save_correct)
    trials.addData('Difference',save_difference)
    trials.addData('touch_delay', touch_delay)
    trials.addData('lick_delay', lick_delay)
    trials.addData('orientation', save_orientation)
    trials.addData('correctstim', correctstim)
    trials.addData('last_choice', last_choice)
    #trials.addData('bias', bias)
    thisExp.nextEntry()
    
# completed 5 repeats of 'trials'

win.close()
core.quit()

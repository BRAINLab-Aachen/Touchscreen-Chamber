# This file is part of the autonomous TouchscreenChamber-HomeCageSystem Project,
# and is released under the "CC BY-NC-SA" LICENSE.
# Copyright 2024 by Gerion Nabbefeld, Department for Neurophysiology at RWTH Aachen University.

# The general structure of this project is based on the TouchScreen Routine published by Wiesbrock et al. 2022.
# The routine has been upgraded to run on newer Windows versions, now integrating movie and audiovisual stimulation.
# Further, the TouchscreenChamber now uses a microcontroller for improved lick-detection, timing and general
# reliability.


# In this file I want to create the new general TouchscreenChamber class that all future Experimental paradigms should
# be built upon.

from os import path, makedirs, getcwd
import numpy as np
from datetime import datetime
import time
from psychopy import visual, core, data, event, logging, sound, gui
# from psychopy.constants import *  # things like STARTED, FINISHED
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
from modules.Serial_functions import search_for_microcontroller_by_name
from modules.functions import calibrate_lick_sensor, phase_0_lick_detection, lick_detection, led_on, led_off, give_reward


class TouchscreenChamber:
    def __init__(self, protocol, expInfo):
        # Inputs
        self.experimenter_name = expInfo["experimenter_name"]
        self.animal_id = expInfo["animal_id"]

        # unpack protocol. We could also use it from the protocol directly, not sure yet what I like better.
        # self.experimental_task = experimental_task
        # self.Protocol_name = protocol.Protocol_name
        # self.ITI = protocol.ITI  # in sec
        self.protocol = protocol

        self.save_folder = path.join(getcwd(), "data")
        self.save_file_basename = ""

        # just to have them declared
        self.serial_obj = object
        self.thisExp = object

        # general setting:
        # ToDo: We should make this a general config for the entire setup instead even above the level of protocols!
        self.valve_duration = 100  # in ms
    #

    def start_session(self):
        # initializations:
        self.initialize_microcontroller(moduleName="HomecageTouchscreenESP32")
        self.initialize_session()

        if self.protocol.present_stimuli:
            self.trial_loop_with_stim()
        else:
            self.trial_loop()
        #

        self.save_experimental_data()
    #

    def initialize_microcontroller(self, moduleName="HomecageTouchscreenESP32"):
        # For now, I assume that only one chamber is connected per PC. If that changes then we would need to give each
        # Microcontroller a unique identifier and search for this specific setup.
        # run setup without Microcontroller
        test_mode = False  # for debugging
        if not test_mode:
            # If memory serves me well, this just throws an error if the module is not found and the program aborts with
            # this as intended
            self.serial_obj = search_for_microcontroller_by_name(moduleName)

            # This takes ~2s. In this time the mouse is not allowed to touch the Spout!
            calibrate_lick_sensor(self.serial_obj)

            # This line is necessary as it sets the desired valve duration for the setup!
            give_reward(self.serial_obj, valve_duration=self.valve_duration)
            print('ready')
        else:
            for _ in range(25):
                print("WARNING! The setup is running in test mode. Only for debugging!")
            #
        #
    #

    def initialize_session(self):
        makedirs(self.save_folder, exist_ok=True)
        dt_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.save_file_basename = path.join(self.save_folder, self.animal_id + "_" + dt_str + "_" + self.experimenter_name)

        self.thisExp = data.ExperimentHandler(runtimeInfo=None,
                                              originPath=None,
                                              savePickle=True,
                                              saveWideText=True,
                                              dataFileName=self.save_file_basename)

        # Not sure if we really need this:
        # # save a log file for detail verbose info
        # logFile = logging.LogFile(filename + '.log', level=logging.EXP)
        # logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

        if self.protocol.present_stimuli:
            self.stimulus_initialization()
        #
    #

    def trial_loop(self):
        # Preallocate
        nax_n_trials = 500

        # trials
        # times = np.zeros((nax_n_trials+1, nax_n_trials))

        # I don't have a good feeling yet for how to generalize the different paradigms. For now, I make the first
        # 2-3 settings individual conditions
        stop_session = False
        if self.protocol.Phase0:
            trialclock = core.Clock()
            # it looks like there is always a general trial loop, with 3 distinct phases:
            #   1. stimulus presentation
            #   2. response detection and reward handling
            #   3. saving trial data

            # It might be easier to change this in range() also to trials like the others to only have a single loop-routine
            for n in range(nax_n_trials):
                # ## STIMULUS PART ## #
                if self.protocol.present_stimuli:
                    # In the pretraining phase this is not done for example
                    pass
                    # self.run_stimuli()
                #

                #
                # ## RESPONSE AND REWARD PART ## #
                # This could be combined into a function with an argument flagging if it's phase 0 or the regular
                # lick-detection
                led_on(serial_obj=self.serial_obj)
                phase_0_lick_detection(serial_obj=self.serial_obj)
                self.times = float(trialclock.getTime())  # get the response time (OS time).
                led_off(serial_obj=self.serial_obj)

                # user feedback
                print(n + 1)

                #
                # ## SAVING PART ## #
                self.save_trial_data()

                # check for quit (the Esc key)
                if event.getKeys(keyList=["escape"]):
                    stop_session = True
                    break
                #

                # check if the session is supposed to be ended
                if stop_session:
                    break
                #

                # 5 sec delay before the LED is turned on again and the mouse is rewarded for the next licks
                # as far as I can tell this is specific to the Phase0, but we could make this an ITI variable that is
                # set to 0 sec if desired.
                time.sleep(self.ITI)
            #
        #
    #

    def stimulus_initialization(self):
        # First create the window
        # Depending on the setup we might need to make some changes here / make those settings
        self.win = visual.Window(size=(640, 480), pos=(300, 0), fullscr=False, screen=1, allowGUI=False, allowStencil=False,
                                 monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
                                 blendMode='avg', useFBO=True, multiSample=True, numSamples=16)

        self.expInfo['frameRate'] = self.win.getActualFrameRate()
        if self.expInfo['frameRate'] != None:
            self.frameDur = 1.0 / round(self.expInfo['frameRate'])
        else:
            self.frameDur = 1.0 / 60.0  # couldn't get a reliable measure so guess
        #

        self.ISI = core.StaticPeriod(win=self.win, screenHz=self.expInfo['frameRate'], name='ISI')
        self.grating = visual.GratingStim(win=self.win, name='grating',
                                          tex=u'sin', mask=None,
                                          ori=0, pos=[0, 0], size=[2, 2], sf=3, phase=0.0,
                                          color=[1, 1, 1], colorSpace='rgb', opacity=1,
                                          texRes=128, interpolate=True, depth=-1.0)

        self.mouse = event.Mouse(win=self.win)
        self.x, self.y = [0, 0]

        # Create some handy timers
        self.globalClock = core.Clock()  # to track the time since experiment started
        self.routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

        max_n_trials = 500
        # set up handler to look after randomisation of conditions etc
        self.trials = data.TrialHandler(nReps=max_n_trials, method='random',
                                        extraInfo=self.expInfo, originPath=-1,
                                        trialList=[None],
                                        seed=None, name='trials')
        self.thisExp.addLoop(self.trials)  # add the loop to the experiment
        self.thisTrial = self.trials.trialList[0]  # so we can initialise stimuli with some values

        self.touch_delay = 0
        self.lick_delay = 0
    #

    # def run_stimuli(self):
    #     pass
    # #

    def trial_loop_with_stim(self):
        # it looks like there is always a general trial loop, with 3 distinct phases:
        #   1. stimulus presentation
        #   2. response detection and reward handling
        #   3. saving trial data
        for thisTrial in self.trials:
            # ## Initialize the next trial ## #
            stop_session = False

            # currentLoop = self.trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial is not None:
                for paramName in thisTrial.keys():
                    exec(paramName + '= thisTrial.' + paramName)

            # ------Prepare to start Routine "trial"-------
            t = 0
            self.trialClock.reset()  # clock
            frameN = -1
            # reset the mouse
            self.mouse.setPos((0, 0))

            # update component parameters for each repeat
            # setup some python lists for storing info about the mouse
            # keep track of which components have finished
            trialComponents = []
            trialComponents.append(self.ISI)
            trialComponents.append(self.grating)
            trialComponents.append(self.mouse)
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
                #
            #

            #
            # ## run current trial ## #
            continueRoutine = True
            while continueRoutine:
                # get current time
                # I'm not sure if the mouse can also be negative to I added the abs() to be sure x+y can't cancel out
                # for anything but x==0 and y==0
                info_mouse = sum(abs(self.mouse.getPos()))
                t = self.trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *grating* updates
                if t >= 0.0 and self.grating.status == NOT_STARTED and info_mouse == 0:
                    self.grating.setAutoDraw(True)
                    # keep track of start time/frame for later
                    self.grating.tStart = t  # underestimates by a little under one frame
                    self.grating.frameNStart = frameN  # exact frame index
                #

                if self.grating.status == STARTED and info_mouse != 0:
                    self.lick_delay = self.trialClock.getTime()
                    timepoint = t
                    n = n + 1
                    print(n)

                    sound_2 = sound.Sound(value='c', secs=0.2, octave=4, stereo=True, volume=1.0, loops=0,
                                          sampleRate=44100, hamming=True, name='', autoLog=True)
                    sound_2.play()

                    self.touch_delay = self.trialClock.getTime()
                    # if not test_mode:
                    led_on(self.serial_obj)
                    stop_session = lick_detection(self.win, self.serial_obj)
                    led_off(self.serial_obj)
                    #

                    continueRoutine = False
                #

                # *mouse* updates
                if t >= 0.0 and self.mouse.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    self.mouse.tStart = t  # underestimates by a little under one frame
                    self.mouse.frameNStart = frameN  # exact frame index
                    self.mouse.status = STARTED
                    event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
                if self.mouse.status == STARTED:  # only update if started and not stopped!
                    buttons = self.mouse.getPressed()
                    if sum(buttons) > 0:  # ie if any button is pressed
                        # abort routine on response
                        continueRoutine = False
                #

                # *ISI* period
                if t >= 0.0 and self.ISI.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    self.ISI.tStart = t  # underestimates by a little under one frame
                    self.ISI.frameNStart = frameN  # exact frame index
                    self.ISI.start(0.5)
                elif self.ISI.status == STARTED:  # one frame should pass before updating params and completing
                    self.ISI.complete()  # finish the static period
                #

                # check for quit (the Esc key)
                if event.getKeys(keyList=["escape"]):
                    stop_session = True
                    break
                #

                if not continueRoutine:
                    # a component has requested a forced-end of Routine
                    break
                #

                # check if all components have finished
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        stop_session = False

                        # This break was now commented before, but I think it should be, so test this
                        # break  # at least one component has not yet finished
                #

                # refresh the screen
                if not stop_session:  # don't flip the monitor if the session is supposed to be stopped
                    # probably make this a more general "stimulus_update()" also for the movies ...
                    self.win.flip()
                #
            # ## End of the trial ## #

            # Trial cleanup and saving
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            #

            # save data from the last trial
            self.save_trial_data()

            # reset
            self.routineTimer.reset()

            if stop_session:
                break
            #
        #
    #

    def save_trial_data(self):
        # In Phase0 no stimulus is presented and not responses are recorded

        # general saves:
        self.thisExp.addData('Protocol_name', self.protocol.Protocol_name)

        if not self.protocol.present_stimuli:
            # Phase0
            self.thisExp.addData('times', self.times)
        else:
            # NOTE: I think getting the mouse here only makes sense in Phase1 and I will likely move this to the
            # Response processing part
            self.x, self.y = self.mouse.getPos()
            self.buttons = self.mouse.getPressed()

            self.trials.addData('mouse.x', self.x)
            self.trials.addData('mouse.y', self.y)
            self.trials.addData('mouse.leftButton', self.buttons[0])
            self.trials.addData('mouse.midButton', self.buttons[1])
            self.trials.addData('mouse.rightButton', self.buttons[2])
            self.trials.addData('touch_delay', self.touch_delay)
            self.trials.addData('lick_delay', self.lick_delay)
        #
        self.thisExp.nextEntry()
    #

    def save_experimental_data(self):
        self.thisExp.saveAsWideText(self.save_file_basename + '.csv')
        self.thisExp.saveAsPickle(self.save_file_basename)
        logging.flush()

        # make sure everything is closed down
        self.thisExp.abort()  # or data files will save again on exit
        # core.quit()
    #
#

#
# class Protocol:
#     def __init__(self):
#         # The same that is saved with the data to make it more easily interpretable
#         self.Protocol_name = "Phase0"
#
#         # I would currently have this as a relatively fixed/hardcoded pretraining phase
#         self.Phase0 = True
#
#         # This is always true except for the very first pretraining sessions
#         self.present_stimuli = False
#
#         # the inter trial interval, added at the end of a given trial
#         self.ITI = 5
#     #
#
#     def load_phase0(self):
#         self.Protocol_name = "Phase0"
#         self.ITI = 5
#         self.Phase0 = True
#         self.present_stimuli = False
#     #
#
#     def load_phase1(self):
#         self.Protocol_name = "Phase1"
#         self.ITI = 5
#         self.Phase0 = False
#         self.present_stimuli = True
#     #
# #
#
#
# if __name__ == "__main__":
#     # I'm still on the fence how exactly I want to organize the protocols
#     # a dict() would be there most flexible, but I would like to define all the arguments that are available/necessary
#     # protocol = {"ITI": 5}
#     protocol_phase0 = Protocol()
#
#     # I could either construct the protocol on the fly (e.g.: class) or save it down completely e.g.: npy/yaml ...
#     # This depends on how I decide to handle the stimulus (long list of target-/distractor-paths or just folder)
#
#
#     # This depends on the GUI we want:
#     if False:
#         # Store info about the experiment session
#         expName = u'Phase_1'  # from the Builder filename that created this script
#         expInfo = {'participant': '', 'session': '001'}
#         dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
#         if not dlg.OK:
#             core.quit()  # user pressed cancel
#         #
#         expInfo['date'] = data.getDateStr()  # add a simple timestamp
#         expInfo['expName'] = expName
#         #
#
#     # Well probably make this a little GUI as well
#     session = TouchscreenChamber(protocol=protocol_phase0, animal_id="0001", experimenter_name="GN")
#
#     # This now runs the session
#     session.start_session()
# #

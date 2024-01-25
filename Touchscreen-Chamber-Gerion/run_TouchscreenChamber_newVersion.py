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
from psychopy import visual, core, data, event, logging, sound, gui
from TouchscreenChamber import TouchscreenChamber


class Protocol:
    def __init__(self):
        # The same that is saved with the data to make it more easily interpretable
        self.Protocol_name = "Phase0"

        # I would currently have this as a relatively fixed/hardcoded pretraining phase
        self.Phase0 = True

        # This is always true except for the very first pretraining sessions
        self.present_stimuli = False

        # the inter trial interval, added at the end of a given trial
        self.ITI = 5
    #

    def load_phase0(self):
        self.Protocol_name = "Phase0"
        self.ITI = 5
        self.Phase0 = True
        self.present_stimuli = False
    #

    def load_phase1(self):
        self.Protocol_name = "Phase1"
        self.ITI = 5
        self.Phase0 = False
        self.present_stimuli = True
    #
#


if __name__ == "__main__":
    experimenter_name = "GN"

    # I'm still on the fence how exactly I want to organize the protocols
    # a dict() would be there most flexible, but I would like to define all the arguments that are available/necessary
    # protocol = {"ITI": 5}
    current_protocol = Protocol()
    current_protocol.load_phase0()

    # I could either construct the protocol on the fly (e.g.: class) or save it down completely e.g.: npy/yaml ...
    # This depends on how I decide to handle the stimulus (long list of target-/distractor-paths or just folder)


    # This depends on the GUI we want:

    # Store info about the experiment session
    expInfo = {'animal_id': '', 'session': '001', 'experimenter_name': experimenter_name}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=current_protocol.Protocol_name)
    if not dlg.OK:
        core.quit()  # user pressed cancel
    #
    # expInfo['date'] = data.getDateStr()  # add a simple timestamp
    # expInfo['expName'] = expName
    # expInfo['experimenter_name'] = experimenter_name
    #

    # Well probably make this a little GUI as well
    session = TouchscreenChamber(protocol=current_protocol, expInfo=expInfo)

    # This now runs the session
    session.start_session()
#

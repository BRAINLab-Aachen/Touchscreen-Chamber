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
from psychopy import core, gui
from modules.TouchscreenChamber import TouchscreenChamber


class Protocol:
    def __init__(self):
        # The same that is saved with the data to make it more easily interpretable
        self.Protocol_name = ""

        # I would currently have this as a relatively fixed/hardcoded pretraining phase
        self.Phase0 = True

        # This is always true except for the very first pretraining sessions
        self.present_stimuli = False

        # Currently plan on defining a fixed list with (Target-Distractor) pairs
        self.stimulus_files = ["", ""]

        # Mice tend to display side-biases (preferring one side over the other or just alteranting).
        # Therefore, usually we include a bias-correction after Knutsen et al. (2006).
        # But I wanted to leave the option to disable this and allow for purely random target-side determination.
        # ToDo: This is not implemented yet, just placeholder!
        self.use_side_bias_correction = True

        # the inter trial interval, added at the end of a given trial
        self.ITI = 5

        # This flag rather there is a correct/incorrect side (left vs. right)
        self.active_target_side = True

        # Define parameters of stimuli to be presented
        self.movie_stimuli = False
        self.movie_audio_on = False

        # Define the maximum number of trials in a session. Inf if not set!
        self.maximum_number_trials = 1000

        self.touchscreen_inverted_screen = True
    #

    def load_phase0(self):
        self.Protocol_name = "Phase0"
        self.ITI = 5
        self.Phase0 = True
        self.present_stimuli = False
        self.active_target_side = False
    #

    def load_phase1(self):
        self.Protocol_name = "Phase1"
        # There was no defined ITI in the previous script, but I think it makes sense to give the mouse time to take the
        # reward before starting the next stimulus
        self.ITI = 2
        self.Phase0 = False
        self.present_stimuli = True
        self.active_target_side = False
    #

    def load_audiovisual_target_only(self):
        # This is the first protocol I set up now that has a correct/incorrect response, with sounds associated as well as a bias-correction ...
        self.Protocol_name = "audiovisual_target_only"
        self.ITI = 2
        self.Phase0 = False
        self.present_stimuli = True
        self.movie_stimuli = True
        self.movie_audio_on = True

        # ToDo: make these relative paths. It wasn't clear yet what the "current directory" is, when we call this from the Hallway.
        rel_path = path.dirname(__file__)
        # self.stimulus_files = [path.join(rel_path, r"stimulus_files\Target_fast.mp4"),
        #                        path.join(rel_path, r"stimulus_files\Distractor_fast.mp4")]
        self.stimulus_files = [path.join(rel_path, r"stimulus_files\Target_fast.mp4"),
                               None]

        self.use_side_bias_correction = True
        self.active_target_side = True  # there is a correct side in this paradigm

        self.maximum_number_trials = 3
    #

    def load_audiovisual_discrim(self):
        # This is the first protocol I set up now that has a correct/incorrect response, with sounds associated as well as a bias-correction ...
        self.Protocol_name = "audiovisual_target_only"
        self.ITI = 2
        self.Phase0 = False
        self.present_stimuli = True
        self.movie_stimuli = True
        self.movie_audio_on = True

        # ToDo: make these relative paths. It wasn't clear yet what the "current directory" is, when we call this from the Hallway.
        rel_path = path.dirname(__file__)
        # self.stimulus_files = [path.join(rel_path, r"stimulus_files\Target_fast.mp4"),
        #                        path.join(rel_path, r"stimulus_files\Distractor_fast.mp4")]
        self.stimulus_files = (path.join(rel_path, r"stimulus_files\Target_fast.mp4"),
                               path.join(rel_path, r"stimulus_files\example50p.mp4"))

        self.use_side_bias_correction = True
        self.active_target_side = True  # there is a correct side in this paradigm

        self.maximum_number_trials = 3
    #
#


if __name__ == "__main__":
    # I'm still on the fence how exactly I want to organize the protocols
    # a dict() would be there most flexible, but I would like to define all the arguments that are available/necessary
    # protocol = {"ITI": 5}
    current_protocol = Protocol()
    # current_protocol.load_phase0()
    # current_protocol.load_phase1()
    current_protocol.load_audiovisual_target_only()

    # I could either construct the protocol on the fly (e.g.: class) or save it down completely e.g.: npy/yaml ...
    # This depends on how I decide to handle the stimulus (long list of target-/distractor-paths or just folder)

    # with the HomeCage I will get them from the call:
    session = TouchscreenChamber(protocol=current_protocol, animal_id="test_mouse")

    # This now runs the session
    session.run_session()
#

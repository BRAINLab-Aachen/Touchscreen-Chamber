from os import path, makedirs
from psychopy import visual, core, data, event, logging, sound, gui
import time
import numpy as np
from modules.Serial_functions import search_for_microcontroller_by_name
from modules.functions import calibrate_lick_sensor, phase_0_lick_detection, led_on, led_off, give_reward


n_trials = 500

# ToDo: We should make this a general config for the entire setup instead of having it in each script!
valve_duration = 100  # in ms

save_data = False

name = 'JL01'
date = '2020-01-13'
root_path = r'C:\data'
makedirs(root_path, exist_ok=True)

# run setup without Microcontroller
test_mode = False
if not test_mode:
    serial_obj = search_for_microcontroller_by_name("HomecageTouchscreenESP32")
    # serial_obj = open_serial(COM_port='COM13', baudrate=9600)

    calibrate_lick_sensor(serial_obj)
    print('ready')

    # This line is necessary as it sets the desired valve duration for the setup!
    give_reward(serial_obj, valve_duration=valve_duration)
else:
    print("WARNING! The setup is running in test mode. Only for debugging!")
#

filename = path.join(root_path, name+date)
thisExp = data.ExperimentHandler(runtimeInfo=None,
                                 originPath=None,
                                 savePickle=True,
                                 saveWideText=True,
                                 dataFileName=filename)

# trials
i = 200
n = 0
# times = np.zeros((n_trials+1, n_trials))
trialclock = core.Clock()
for n in range(n_trials):
    led_on(serial_obj=serial_obj)
    phase_0_lick_detection(serial_obj=serial_obj)
    print(n+1)
    times = float(trialclock.getTime())
    led_off(serial_obj=serial_obj)
    thisExp.addData('times', times)
    thisExp.nextEntry()
    time.sleep(5)
#


if save_data:
    thisExp.saveAsWideText(filename+'.csv')
    thisExp.saveAsPickle(filename)
    logging.flush()
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit

    # To keep the prompt open for the user
    while True:
        time.sleep(1.)
    #
    # core.quit()
#

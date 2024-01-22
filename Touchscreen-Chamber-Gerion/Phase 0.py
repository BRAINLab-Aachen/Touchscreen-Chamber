# from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from os import path, makedirs
from psychopy import visual, core, data, event, logging, sound, gui
import time
import numpy as np
from modules.Serial_functions import open_serial, send_data_until_confirmation
from modules.functions import calibrate_lick_sensor, phase_0_lick_detection, led_on, led_off, give_reward

n_trials = 500
valve_duration = 100  # in ms

root_path = r'C:\data'
name = 'JL01'
date = '2020-01-13'

try:
    makedirs(root_path)
except:
    pass
#

test_mode = False
if not test_mode:
    serial_obj = open_serial(COM_port='COM13', baudrate=9600)
    # ADJUST_TOUCHLEVEL = 75
    # send_data_until_confirmation(serial_obj, header_byte=ADJUST_TOUCHLEVEL, data=[3])
    calibrate_lick_sensor(serial_obj)
    print('ready')

    give_reward(serial_obj, valve_duration=valve_duration)
#

thisExp = data.ExperimentHandler(runtimeInfo=None,
                                 originPath=None,
                                 savePickle=True,
                                 saveWideText=True,
                                 dataFileName=path.join(root_path, name+date))

# trials
i = 200
n = 0
# times = np.zeros((n_trials+1, n_trials))
trialclock = core.Clock()
for n in range(n_trials):
    led_on(serial_obj=serial_obj)
    phase_0_lick_detection(serial_obj=serial_obj, valve_duration=valve_duration)
    print(n+1)
    times = float(trialclock.getTime())
    led_off(serial_obj=serial_obj)
    thisExp.addData('times', times)
    thisExp.nextEntry()
    time.sleep(5)
#


# thisExp.addData('times',times)
# thisExp.nextEntry()
# np.savetxt('C:\Dokumente und Einstellungen\Michael\Desktopname\Daten\\'+name+date+'.csv', times, delimiter=',')
# print num
# plt.plot(num,times,'r-')

if False:
    thisExp.saveAsWideText(filename+'.csv')
    thisExp.saveAsPickle(filename)
    logging.flush()
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit
    while True:
        time.sleep(1.)
    #
    # core.quit()
#

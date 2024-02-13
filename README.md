# Touchscreen-Chamber

This repository contains information about a open-source touchscreen chamber for operant conditioning. 
Here, we want to share all relevant information about the touchscreen chamber used in the publication "A flexible python-based touchscreen chamber for operant conditioning reveals improved visual perception of cardinal orientations in mice" by Wiesbrock et al. 2022 (Link). 

Parts of the scripts are based on the Psychopy-Toolkit by Jonathan Peirce (https://www.psychopy.org/)


# Overview

Operant conditioning is crucial technique to quantatitate the perception of animals. We propose this touchscreen chamber to support open science and reproducibility. 
The scripts can be adapted to different experimental situations. For now, we propose pretraining procedures, so the animals can familarize themselves with the touchscreen chamber. Then there are three different approaches presented: Visual discrimination between different orientateted sine-wave gratings, a newly developed parallel visual discrimination test and, also new in the field of the mouse visual system, a staircase procedure with an adapting level of difficulty. 

# Requirements

|Part|Price|
|---|---|
|Measurement Computing 1208LS (Measurement Computing GmbH) | 125 €|
|Magnet ventile (SMC Pneumatik, 9900001809231)|50 €|
|PVC plates| 30 € |
|Display 11 inch (ELO touch 1002L)| 70 €|
|Infrared Frame (NJY touch, Guangdong, China)| 115 €|
|Clipper Box (Bauhaus)| 12 €|
|Logitech Z120 Speaker (Conrad Electronics)|17 €|
|Laptop| 210 €|
|Relais| 2 €|
|Cables, screws, tubes, piezo (Conrad electronics)|15 €|
|Webcam (Logitech C920)| 25 €|
|Dynavox TC-750 Amplifier| 28 €|
|Sum:| 699| 



# Assembly of the Hardware

First of all, the basis framework of the touchscreen chamber is needed (see https://github.com/BRAINLab-Aachen/Touchscreen-Chamber/blob/master/3d/TC.stl). We suggest to build it from single PVC plates assmebled with screws. The display holder needs to be two-parted according to the specific dimensions of the display and the infrared frame. The backside needs a fitting socket for the display and all cables as well as for the infrared frame. The frontside fixates the components and needs a hole, so the screen is visible. Note that the screenholder must not touch the glass of the infrared frame. On the opposite side of the screenholder, a hole needs to be drilled for the water spout in a height of 2 cm. The diameter of the hole should allow some minor movement of the water spout to get a stronger signal at the Piezo element. Above, a second hole is needed for a green LED light. The LED light (under consideration of specific resistances) needs to be connected to the DAQ's digital port.

The lick detection consists of a water spout, a piezo element, an amplifier (we used Dynavox TC-750 Amplifier) and a DAQ (Measurement Computing 1208LS (Measurement Computing GmbH) ). The water spout should be long enough to attach the piezo element to it outside the basic framework. According to the specific piezo elements used, it needs to be connected to the amplifier input. The amplifier output is connected to the analog ports of the DAQ. Using the software, delivered with the DAQ it should be tested, if it is visible, when the piezo element is moved. 

The water delivery system consists of a magnet ventile, a relais and the DAQ. The digital port of the DAQ needs to be connected to the relais, while the relais is connected to power and the magnet ventile. By getting the signal from the digital port, the cirquit is closed and the magnet ventile opens. A water tank (we use 10 ml syringes without a cannula) needs to be connected with a fitting tube to the intake side of the ventile. The water spout needs to be connected via a tube to the outtake side of the ventile. Important: Please take the specifications of single parts into consideration. Magnet ventiles and relais from different vendors can have a large variability in terms of power and voltage. 

The dimensions of the basis framework fits into a larger variety of clipper boxes. This is the "basic" solution. If you are running experiments, which needs a higher level of silence while they are in a not-so-quite environment, please consider the use of a proper sound attenuation box. 

## Installation ##
1. In this Project an ESP32 with a CP2102 chip is used. This requires the installation of the appropriate USB-drive:
"https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads"

2. Futher the Arduino IDE is required to upload the code to the ESP32:
"https://www.arduino.cc/en/software"

3. The ESP32 Board need to be added to Arduino IDE. See instructions here: "https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/"
In short: Go to "File>Preferences", then add "https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json" under “Additional Board Manager URLs”


# Software

At the moment the Touchscreen Chamber is running with Python 2.7. Since not everyone is using Python2, we suggest the following to create a dedicated environment:

conda create --name TouchscreenChamber Python==2.7
pip install Psychopy==1.83.04

For the installation one more package is needed. First of all for the control of the DAQ via Python the Package UniversalLibrary is needed, which can be found here: https://pypi.org/project/PyUniversalLibrary/#files or pip install mcculw

To prepare your experiments, you need to start piezo calibration.py first. This script reads the signal from the piezo element. According to the specific model of your piezo element, a daily calibration is probably needed. The threshold for a touch at the lick detection needs to be adapted in following experimental scripts.

The pretraining consists of two scripts. For autoreward.py, the screen can be deactivated. In this phase, the green led light is activated, when a reward is available. After the mouse collected the reward, the green light turns off and turns on again after a predefined timeout. After 2-3 sessions, the mouse should have collected at least one reward per minute and can proceed to the next stage. The next step is the touch training (touchtraining.py), where the animal learns to touch the screen in order to get a reward. Again, it turns out to be benefitial, when the mice are able to complete one trial per minute on two consecutive sessions. 

Congratulations! Your mouse is ready for an operant conditioning experiment. We propose different orientation discrimination tasks (staircase, visual discrimination and parallel visual discrimination learning). Using the built-in GUI of Psychopy, it is also possible to create a large variety of different tasks and use it in the touchscreen chamber. The specific functions can be taken from the orientation discrimination tasks.

# Future

Stay tuned for the Python 3 upgrade and Arduino support in the future.  



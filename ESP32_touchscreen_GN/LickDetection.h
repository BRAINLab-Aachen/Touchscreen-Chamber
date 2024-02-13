/*
  Task.h - Library to run MS_Task_V2_0.
  Created by Gerion Nabbefeld, October 8, 2020.
  Released into the public domain.
*/

#ifndef LickDetection_h
#define LickDetection_h

#include "Arduino.h"

class LickDetection {
  public:
    // constructor
    LickDetection(int SPOUTSENSOR);

    // Call function
    void ReadTouchSensors();

    // adjustment functions
    void command_AdjustTouchLevel(float new_threshold);

    // resets the counters for the next trials
    void reset_response_counter();

    // Touch variables
    unsigned int touchAdjustDur = 2000; // time used to re-adjust touch levels if neccessary. This will infer the mean (in the first hald) and standard deviation (in the second half) of the read-noise to infer decent thresholds for touch.
    int touchThresh = 3; // threshold for touch event in standard deviation units.
    int touchThreshOffset = 1; // additional offset for touch threshold.
    bool touchAdjust = true; // flag to determine values to detect touches. Do this on startup.
    float touchData[2] = { 0, 0 }; // current values for the four touch lines (left spout, right spout, left, handle, right handle)
    float meanTouchVals[4] = { 0, 0, 0, 0 }; // mean values for the four touch lines (left spout, right spout, left, handle, right handle)
    float stdTouchVals[4] = { 0, 0, 0, 0 }; // stand deviation values for the four touch lines (left spout, right spout, left, handle, right handle)
    float touchVal = 0; // temporary variable for usb communication
    long int sampleCnt[2] = { 0, 0 }; // counter for samples during touch adjustment

    // State Values
    bool spoutTouch = false; // flag to indicate that left spout is touched

  private:
    // PINs
    int _SPOUTSENSOR; // Spout Left

    //
    unsigned int sRateLicks = 5;  // This is the minimum duration of lick events that are send to bpod.

    // state variables to ensure that 
    bool touch_state = false;

    // Clocks
    unsigned long spoutClocker; // timer to measure duration of left lick
    unsigned long adjustClocker; // timer for re-adjustment of touch lines

};

#endif

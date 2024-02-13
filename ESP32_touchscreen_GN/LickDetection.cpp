/*
  Morse.cpp - Library for flashing Morse code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/

#include "Arduino.h"
#include "LickDetection.h"

LickDetection::LickDetection(int SPOUTSENSOR) {
  // PINs
  _SPOUTSENSOR = SPOUTSENSOR; // Spout
//  pinMode(_SPOUTSENSOR, INPUT);

  // Clocks
  adjustClocker = millis(); // timer for re-adjustment of touch lines
  spoutClocker = millis(); // timer to measure duration of left lick
}

void LickDetection::ReadTouchSensors() {
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Read Data from TouchPins ////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////
  touchData[0] = touchRead(_SPOUTSENSOR);
//  touchData[0] = analogRead(_SPOUTSENSOR);
//  Serial.println(touchData[0]);

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Recalibrate TouchSensors upon request ///////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // recompute estimates for mean and standard deviation in each touch line and updates thresholds accordingly
  if (touchAdjust) {
    ++sampleCnt[0];
    for (int i = 0; i < 1; i++) {
      meanTouchVals[i] = meanTouchVals[i] + ((touchData[i] - meanTouchVals[i])/sampleCnt[0]); // update mean
    }
    if ((millis() - adjustClocker) > (touchAdjustDur/2)) { // second part of adjustment: get summed variance
      ++sampleCnt[1];
      for (int i = 0; i < 1; i++) {
        stdTouchVals[i] = stdTouchVals[i] + sq(touchData[i] - meanTouchVals[i]); // update standard deviation (summed variance here)
      }
    }
    if ((millis() - adjustClocker) > touchAdjustDur) {  // done with adjustment
      for (int i = 0; i < 1; i++) {
         stdTouchVals[i] = sqrt(stdTouchVals[i]/sampleCnt[1]) + touchThreshOffset; // compute standard deviation from summed variance
      }
      touchAdjust = false;
    }
  }

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // check touch lines and create according output ///////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////
  if (!touchAdjust) {
    // ESP32 inverts the lick detection. Values closer to 0 mean lick!
    if (touchData[0] < (meanTouchVals[0]-(stdTouchVals[0]*touchThresh))) { // signal above 'stdTouchVals' standard deviations indicate lick event. only when spouts dont move.
      spoutClocker = millis(); //update time when spout was last touched
      touch_state = true;
      spoutTouch = true;
    }
    else {
      if ((millis() - spoutClocker) >= sRateLicks) { // check when lever was last touched and set output to low if it happened too long ago.

        if (touch_state) {
          touch_state = false;
          spoutTouch = false;
        }
      }
    }
  }
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////
}

void LickDetection::reset_response_counter() {
  spoutTouch = false;
  touch_state = false;
}

void LickDetection::command_AdjustTouchLevel(float new_threshold) {
  touchThresh = new_threshold;
  touchAdjust = true; // flag to adjust touchlevels
  adjustClocker = millis();
  sampleCnt[0] = 0; sampleCnt[1] = 0; // reset counter
  meanTouchVals[0] = 0; meanTouchVals[1] = 0; meanTouchVals[2] = 0; meanTouchVals[3] = 0; // reset mean values
  stdTouchVals[0] = 0; stdTouchVals[1] = 0; stdTouchVals[2] = 0; stdTouchVals[3] = 0; // reset std values
}

/*
  Task.h - Library to run MS_Task_V2_0.
  Created by Gerion Nabbefeld, October 8, 2020.
  Released into the public domain.
*/

#ifndef TimedDigitalPulse_h
#define TimedDigitalPulse_h

#include "Arduino.h"

class TimedDigitalPulse {
  public:
    // constructor
    TimedDigitalPulse() {};
    //TimedDigitalPulse(int PIN, unsigned long duration_in_us);

    //// define PIN and pulse duration in us
    void configure(int PIN, unsigned long duration_in_us);
    void change_duration(unsigned long duration_in_us);

    // start Pulse by switching PIN to HIGH
	void sendTrigger();

    // check if Pulse is finished and switch Line to LOW
    void update();

    // Signal definition
    int _PIN;
    unsigned int _duration;

    // State Variables
    bool state;

  private:
	// Clocks
    unsigned long _clock;
};

#endif

/*
  Morse.cpp - Library for flashing Morse code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/

#include "Arduino.h"
#include "TimedDigitalPulse.h"

void TimedDigitalPulse::configure(int PIN, unsigned long duration_in_us) {
  // define PIN and pulse duration in us
  _PIN = PIN;
  _duration = duration_in_us;
    
  // Initialize PIN
  pinMode(_PIN, OUTPUT);
  digitalWrite(_PIN, LOW);
  state = false;

  //// Clocks
  _clock = micros();
}

void TimedDigitalPulse::change_duration(unsigned long duration_in_us) {
  _duration = duration_in_us;
}

void TimedDigitalPulse::sendTrigger() {
  // start Pulse by switching PIN to HIGH
  state = true;
  _clock = micros();
  digitalWrite(_PIN, HIGH);
}

void TimedDigitalPulse::update() {
  // check if Pulse is finished and switch Line to 
  if (state) {
    if (micros() - _clock >= _duration) {
      state = false;
      digitalWrite(_PIN, LOW);
    }
  }
}

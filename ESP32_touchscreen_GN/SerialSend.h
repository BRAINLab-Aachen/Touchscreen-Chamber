#ifndef SerialSend_h
#define SerialSend_h

#include "Arduino.h"

class SerialSend {
  public:
    SerialSend() { Clock = millis(); } // constructor
	  void configure(int byte_value, unsigned int timeout=200); // replacement for the constructor
	  void send(); // send the byte over Serial to the PC
    void update(); // wait for confirmation from PC and resend if timeout
    
    // After every trial set this to false, so this function doens't blcok in case the confirmation was missed
    bool waiting_for_confirmation = false;

  private:
    int _byte_value; // byte to send
    unsigned int _timeout; // to wait for confirmation before resend request in ms

	  // Clocks
    unsigned long Clock;
};

#endif

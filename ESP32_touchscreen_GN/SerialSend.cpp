#include "Arduino.h"
#include "SerialSend.h"

void SerialSend::configure(int byte_value, unsigned int timeout) {
  _byte_value = byte_value;
  _timeout = timeout;
  waiting_for_confirmation = false;
}

void SerialSend::send() {
  // send the byte over Serial to the PC
  Serial.write(_byte_value);
  Clock = millis();
  waiting_for_confirmation = true;
}

void SerialSend::update() {
  // wait for confirmation from PC and resend if timeout
  if (waiting_for_confirmation) {
    if (millis() - Clock >= _timeout) {
      send();
    }
  }
}

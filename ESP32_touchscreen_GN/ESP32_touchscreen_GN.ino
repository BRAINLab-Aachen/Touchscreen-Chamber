#include "Arduino.h"
#include "LickDetection.h"
#include "TimedDigitalPulse.h"
#include "SerialSend.h"

////////////////////////////////////////////////////
// LickDetection ///////////////////////////////////
////////////////////////////////////////////////////
// Inputs for lick sensors
#define SPOUTSENSOR 13 // touch line for left spout

// Init LickDetection
LickDetection lick(SPOUTSENSOR);
LickDetection* lick_ptr = &lick;


////////////////////////////////////////////////////
// Experiment //////////////////////////////////////
////////////////////////////////////////////////////
// PINs to control Setup
#define PIN_VALVE 12 // Water valve
#define LED_PIN 14

SerialSend RespondedSerialObject;
TimedDigitalPulse VALVE;

////////////////////////////////////////////////////
// USB Serial Communication ////////////////////////
////////////////////////////////////////////////////
// Byte codes for serial communication
// inputs
#define ADJUST_TOUCHLEVEL 75 // identifier to re-adjust threshold for touch sensors. Will sample over 1 second of data to infer mean/std of measurements.

#define FLUSH_VALVE 100 // flush valves outside of the experiment using this command
#define LED_ON 101
#define LED_OFF 102
#define WAIT_FOR_LICK_REWARDED 103
#define WAIT_FOR_LICK_NOT_REWARDED 104

#define GOT_BYTE 14 // positive handshake for bpod commands
#define DID_ABORT 15 // negative handshake for bpod commands

// Serial COM variables
unsigned long serialClocker = millis();
int FSMheader = 0;
bool midRead = false;
bool read_msg_length = false;
float temp[22]; // temporary variable for general purposes

unsigned long lickClocker = millis();

unsigned long open_duration = 75070;  // in us

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void setup() {
  Serial.begin(9600);

  pinMode(LED_PIN, OUTPUT);
//  pinMode(PIN_VALVE, OUTPUT);

  VALVE.configure(PIN_VALVE, open_duration);

  RespondedSerialObject.configure(FLUSH_VALVE);
}

void loop() {
  ReadSerialCommunication();
  lick_ptr->ReadTouchSensors();

  VALVE.update();
  RespondedSerialObject.update();
} // end of void loop

void ReadSerialCommunication() {
  // Serial Communication over USB
  // Main purpose is to start a new trial
  if (Serial.available() > 0) {
    if (!midRead) {
      FSMheader = Serial.read();
      midRead = 1; // flag for current reading of serial information
      serialClocker = millis(); // counter to make sure that all serial information arrives within a reasonable time frame (currently 100ms)
      read_msg_length = false;
    }
    if (midRead) {
      if (FSMheader == FLUSH_VALVE) {
        if (Serial.available() > 1) {
          unsigned long open_duration = readSerialChar(Serial.read());
          Serial.write(GOT_BYTE); midRead = 0;
          VALVE.change_duration(open_duration);
          VALVE.sendTrigger();
          midRead = 0;
        }
      }
      else if (FSMheader == ADJUST_TOUCHLEVEL) { // check mean and std for all touch lines to adjust thresholds
        if (Serial.available() > 1) {
          lick.command_AdjustTouchLevel(readSerialChar(Serial.read()));
          Serial.write(GOT_BYTE); midRead = 0;
        }
        else if ((millis() - serialClocker) >= 100) {
          Serial.write(DID_ABORT); midRead = 0;
        }
      }
      else if (FSMheader == LED_ON) {
        Serial.write(GOT_BYTE); midRead = 0;
        digitalWrite(LED_PIN, HIGH);
        midRead = 0;
      }
      else if (FSMheader == LED_OFF) {
        Serial.write(GOT_BYTE); midRead = 0;
        digitalWrite(LED_PIN, LOW);
        midRead = 0;
      }
      else if (FSMheader == WAIT_FOR_LICK_REWARDED) {
        if (Serial.available() > 1) {
          unsigned long duration = readSerialChar(Serial.read());
//          unsigned long open_duration = readSerialChar(Serial.read());
          Serial.write(GOT_BYTE); midRead = 0;
//          VALVE.change_duration(open_duration);
          
          lickClocker = millis();
          while (millis() - lickClocker < duration) {
            lick_ptr->ReadTouchSensors();
  
            if (lick_ptr->spoutTouch) {
              VALVE.sendTrigger();
              RespondedSerialObject.send();
              break;
            }
          }
          digitalWrite(LED_PIN, LOW);
          midRead = 0;
        }
        else if ((millis() - serialClocker) >= 100) {
          Serial.write(DID_ABORT); midRead = 0;
        }
      }
      else if (FSMheader == WAIT_FOR_LICK_NOT_REWARDED) {
        if (Serial.available() > 1) {
          unsigned long duration = readSerialChar(Serial.read());
//          unsigned long open_duration = readSerialChar(Serial.read());
          Serial.write(GOT_BYTE); midRead = 0;
  
          lickClocker = millis();
          while (millis() - lickClocker < duration) {          
            lick_ptr->ReadTouchSensors();
  
            if (lick_ptr->spoutTouch) {
              RespondedSerialObject.send();
              break;
            }
          }
          digitalWrite(LED_PIN, LOW);
          midRead = 0;
        }
        else if ((millis() - serialClocker) >= 100) {
          Serial.write(DID_ABORT); midRead = 0;
        }
      }
  
      
  
      else if (FSMheader == GOT_BYTE){
        // The Serial COM waiting for confirmation inside Experiment makes Issues.
        // This is not elegant, but I'm assuming now that any GOT_BYTE received here is in response to the Stimulus/Response signals send inside Experiment
        RespondedSerialObject.waiting_for_confirmation = false;
        //Serial.write(69);
        midRead = 0;
      }
      else {
        //flush the Serial to be ready for new data
        while (Serial.available() > 0) {
          Serial.read();
        }
        midRead = 0;
  
  //      //send abort to request resend
  //      Serial.write(DID_ABORT); midRead = 0;
      }
    }
  }

  if (midRead && ((millis() - serialClocker) >= 100)) {
      //flush the Serial to be ready for new data
      while (Serial.available() > 0) {
        Serial.read();
      }

      //send abort to request resend
      Serial.write(DID_ABORT); midRead = 0;
  }
}

float readSerialChar(byte currentRead){
  float currentVar = 0;
  byte cBytes[currentRead-1]; // current byte
  int preDot = currentRead; // indicates how many characters there are before a dot
  int cnt = 0; // character counter

  if (currentRead == 1){
    currentVar = Serial.read() -'0'; 
  }

  else {
    for (int i = 0; i < currentRead; i++) {
      cBytes[i] = Serial.read(); // go through all characters and check for dot or non-numeric characters
      if (cBytes[i] == '.') {cBytes[i] = '0'; preDot = i;}
      if (cBytes[i] < '0') {cBytes[i] = '0';}
      if (cBytes[i] > '9') {cBytes[i] = '9';}
    }
  
    // go through all characters to create new number
    if (currentRead > 1) {
      for (int i = preDot-1; i >= 1; i--) {
        currentVar = currentVar + ((cBytes[cnt]-'0') * pow(10,i));
        cnt++;
      }
    }
    currentVar = currentVar + (cBytes[cnt] -'0'); 
    cnt++;
  
    // add numbers after the dot
    if (preDot != currentRead){
      for (int i = 0; i < (currentRead-preDot); i++) {
        currentVar = currentVar + ((cBytes[cnt]-'0') / pow(10,i));
        cnt++;
      }
    }
  }
  return currentVar;
}

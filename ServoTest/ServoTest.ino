// This script tests communciation between the PC and the arduino, as well as the function of the servo.

#include <Servo.h>

Servo J0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  J0.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() > 0){
    int ms = Serial.parseInt();
    J0.writeMicroseconds(ms);
  }
}

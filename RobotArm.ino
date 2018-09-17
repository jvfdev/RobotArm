/* Arduino Robot Arm Code
 * Designed for RobotArmGUI Version 1.0 
 */

#include <Servo.h>

String str;
Servo J0, J1, J2, J3, J4;

void setup() {
  // put your setup code here, to run once:

  J0.attach(13);
  J1.attach(12);
  J2.attach(11);
  J3.attach(10);
  J4.attach(9);
  Serial.begin(9600);
  Serial.println("Connection Established");

  J0.writeMicroseconds(1475);
  J1.writeMicroseconds(1900);
  J2.writeMicroseconds(1800);
  J3.writeMicroseconds(1000);
 J4.writeMicroseconds(1900);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char serialData = Serial.read();
    if (serialData == ',') {
      //Serial.print("foo");
      int n = str.toInt();
      if (str.indexOf('a') > 0) J0.writeMicroseconds(n);
      if (str.indexOf('b') > 0) J1.writeMicroseconds(n);
      if (str.indexOf('c') > 0) J2.writeMicroseconds(n);
      if (str.indexOf('d') > 0) J3.writeMicroseconds(n);
      if (str.indexOf('e') > 0) J4.writeMicroseconds(n);
      else {
        Serial.println(str);
      }
      str = "";
    }
    else {
      str += serialData;
    }


  } // end ifSerialAvailable

}

/* Arduino Robot Arm Code
   Designed for RobotArmGUI Version 1.1
*/

#include <Servo.h>

String str;
Servo J0, J1, J2, J3, J4;
int us_new[5];
int us_old[] = {1475, 1742, 2049, 981, 1100};

void setup() {
  // put your setup code here, to run once:

  J0.attach(13);
  J1.attach(12);
  J2.attach(11);
  J3.attach(10);
  J4.attach(9);
  Serial.begin(9600);
  Serial.println("Connection Established");

  J0.writeMicroseconds(us_old[0]);
  J1.writeMicroseconds(us_old[1]);
  J2.writeMicroseconds(us_old[2]);
  J3.writeMicroseconds(us_old[3]);
  J4.writeMicroseconds(us_old[4]);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char serialData = Serial.read();

    if (serialData == ',') {
      int n = str.toInt();
      if (str.indexOf('a') > 0) us_new[0] = n;
      if (str.indexOf('b') > 0) us_new[1] = n;
      if (str.indexOf('c') > 0) us_new[2] = n;
      if (str.indexOf('d') > 0) us_new[3] = n;
      if (str.indexOf('e') > 0) us_new[4] = n;
      else {
        // do nothing
      }
      str = "";
    }
    else if (serialData == ';') {
      moveArm(us_new, us_old);
      serialData = "";
    }
    else {
      str += serialData;
    }


  } // end ifSerialAvailable

}

void moveArm(int x_new[5], int x_old[5]) {
  Serial.println("test4");
  int t0 = millis();
  float v = 100.0; // us/s angular velocity (assumes 10 us/deg)

  float dt = 0;
  float maxdt = 0;
  for (int i = 0; i < 5; i++) {
    dt = abs((x_new[i] - x_old[i])) / v;
    if (dt > maxdt) {
      maxdt = dt;
    }
  }
  dt = maxdt;
  int t = 0;
  if ( dt != 0) {
    while (t / 1000.0 <= abs(dt)) {
      t = millis() - t0;
      J0.writeMicroseconds(int((x_new[0] - x_old[0]) / dt * t / 1000.0 + x_old[0]));
      J1.writeMicroseconds(int((x_new[1] - x_old[1]) / dt * t / 1000.0 + x_old[1]));
      J2.writeMicroseconds(int((x_new[2] - x_old[2]) / dt * t / 1000.0 + x_old[2]));
      J3.writeMicroseconds(int((x_new[3] - x_old[3]) / dt * t / 1000.0 + x_old[3]));
      J4.writeMicroseconds(int((x_new[4] - x_old[4]) / dt * t / 1000.0 + x_old[4]));
    }
  }

  for (int k = 0; k < 5; k++) {
    x_old[k] = x_new[k];
  }


}


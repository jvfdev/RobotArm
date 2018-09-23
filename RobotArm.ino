/* Arduino Robot Arm Code
   Designed for RobotArmGUI Version 1.1
*/

#include <Servo.h>

String str;
Servo J0, J1, J2, J3, J4;
int us_new[] = {1475, 1742, 2049, 981, 1100};
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

  J0.writeMicroseconds(us_new[0]);
  J1.writeMicroseconds(us_new[1]);
  J2.writeMicroseconds(us_new[2]);
  J3.writeMicroseconds(us_new[3]);
  J4.writeMicroseconds(us_new[4]);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char serialData = Serial.read();
    //    Serial.print("Character input: ");
    //    Serial.println(serialData);
    if (serialData == ',') {
      //Serial.print("foo");
      int n = str.toInt();
      //      Serial.println("test1");
      if (str.indexOf('a') > 0) us_new[0] = n;
      if (str.indexOf('b') > 0) us_new[1] = n;
      if (str.indexOf('c') > 0) us_new[2] = n;
      if (str.indexOf('d') > 0) us_new[3] = n;
      if (str.indexOf('e') > 0) us_new[4] = n;
      //      if (str.indexOf('a') > 0) J0.writeMicroseconds(n);
      //      if (str.indexOf('b') > 0) J1.writeMicroseconds(n);
      //      if (str.indexOf('c') > 0) J2.writeMicroseconds(n);
      //      if (str.indexOf('d') > 0) J3.writeMicroseconds(n);
      //      if (str.indexOf('e') > 0) J4.writeMicroseconds(n);
      else {
        //        Serial.println(str);
        //        Serial.println(us_new[0]);
      }
      str = "";
    }
    else if (serialData == ';') {
      Serial.println("test2");
      moveArm(us_new, us_old);
      serialData = "";
    }
    else {
      //      Serial.println("test3");
      str += serialData;
    }


  } // end ifSerialAvailable

}

void moveArm(int x_new[5], int x_old[5]) {
  Serial.println("test4");
  int t0 = millis();
  float v = 100.0; // us/s angular velocity (assumes 10 us/deg)

  float dt = abs(x_new[0] - x_old[0]) / v;
  Serial.print("dt: ");
  Serial.println(dt);
  int t = 0;
  if ( dt != 0) {
    while (t / 1000.0 <= dt) {
      t = millis() - t0;
      int y = (x_new[0] - x_old[0]) / dt * t / 1000.0 + x_old[0];
      Serial.print("us:");
      Serial.println(y);
      J0.writeMicroseconds(y);
    }
  }
  Serial.println("aqui");
  x_old[0] = x_new[0];
  //  Serial.print
  Serial.println(x_old[0]);
  //  y = v*t+x_old[0];

  //  J0.writeMicroseconds(x_new[0]);
  //  J1.writeMicroseconds(x_new[1]);
  //  J2.writeMicroseconds(x_new[2]);
  //  J3.writeMicroseconds(x_new[3]);
  //  J4.writeMicroseconds(x_new[4]);
}


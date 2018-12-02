/* Arduino Robot Arm Code
   Designed for RobotArmGUI Version 2.0
   Versions --
   2.0 - Uses inverse kinematics to drive arm, input is desired end effector position
*/

#include <Servo.h>
#include <math.h>

String str;
Servo J0, J1, J2, J3, J4;
int us_new[5];
int us_old[] = {1475, 1742, 2049, 981, 1100};
float X_new[] = {230.0, 50.0, 0.0, 90.0, 10.0}; // R Z phi theta gripper
float X_old[] = {230.0, 50.0, 0.0, 90.0, 11.0}; // this has to be different for initial movement of moveArm

const float L0 = 50.65;
const float L1 = 114.8;
const float L2 = 113.55;
const float L3 = 110.0;

void setup() {

  J0.attach(13);
  J1.attach(12);
  J2.attach(11);
  J3.attach(10);
  J4.attach(9);
  Serial.begin(9600);
  Serial.println("Connection Established");
  moveArm(X_new, X_old);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char serialData = Serial.read();

    if (serialData == ',') {
      int n = str.toInt();
      if (str.indexOf('R') > 0) X_new[0] = n;
      if (str.indexOf('Z') > 0) X_new[1] = n;
      if (str.indexOf('P') > 0) X_new[2] = n;
      if (str.indexOf('T') > 0) X_new[3] = n;
      if (str.indexOf('G') > 0) X_new[4] = n;

      else {
        // do nothing
      }
      str = "";
    }
    else if (serialData == ';') {
      moveArm(X_new, X_old);
      serialData = "";
      for (int k = 0; k < 5; k++) {
        X_old[k] = X_new[k];
      }
    }
    else {
      str += serialData;
    }


  } // end ifSerialAvailable

}


void moveArm(float x_new[5], float x_old[5]) {
  float v = 15.0; // approximate end effector velocity, mm/s

  //total distance to travel (technically not the true distance, but accounts for all joints)
  float D = sqrt( sq(x_new[0] - x_old[0]) + sq(x_new[1] - x_old[1]) + sq(x_new[2] - x_old[2]) + sq(x_new[3] - x_old[3]) + sq(x_new[4] - x_old[4])  );

  // time required
  float dt = D / v;

  // slopes of linear velocity profiles
  float mr = (X_new[0] - X_old[0]) / dt;
  float mz = (X_new[1] - X_old[1]) / dt;
  float mp = (X_new[2] - X_old[2]) / dt;
  float mt = (X_new[3] - X_old[3]) / dt;
  float mg = (X_new[4] - X_old[4]) / dt;

  if ( dt != 0) {
    unsigned long t0 = millis();
    float t = 0.0;
    while (t  < dt) {
      t = (millis() - t0) / 1000.0;
      float r = mr * t + X_old[0];
      float z = mz * t + X_old[1];
      float phi = deg2rad(mp * t + X_old[2]);
      float theta = mt * t + X_old[3];
      float grip = mg * t + X_old[4];

      float rc = r - L3 * cos(phi);
      float zc = z - L3 * sin(phi);
      float d = sqrt( sq(rc) + sq(zc - L0) );

      float theta2 = acos( (sq(L1) + sq(L2) - sq(d)) / (2.0 * L1 * L2));
      float theta1 = atan( (zc - L0) / rc ) + acos( (sq(d) + sq(L1) - sq(L2) ) / (2.0 * d * L1));
      float theta3 = theta1 + theta2 - phi;

      int  us0 = angle2us(constrain(theta, 5, 175), 9.444, 625);
      int  us1 = angle2us(constrain(rad2deg(theta1), 0, 180), -9.7222, 2325);
      int  us2 = angle2us(constrain(rad2deg(theta2), 25, 180), -8.0556, 2250);
      int  us3 = angle2us(constrain(rad2deg(theta3), 80, 250), 10.2778, -150);
      int  us4 = angle2us(constrain(grip, 0, 250), 5.000, 1050);

      J0.writeMicroseconds(us0);
      J1.writeMicroseconds(us1);
      J2.writeMicroseconds(us2);
      J3.writeMicroseconds(us3);
      J4.writeMicroseconds(us4);
    }
  }
}

float deg2rad(float x) {
  return M_PI * x / 180;
}

float rad2deg(float x) {
  return 180 * x / M_PI;
}

float angle2us(float deg, float m, float b) {
  return round(deg * m + b);
}

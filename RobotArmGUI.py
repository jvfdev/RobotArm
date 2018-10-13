"""
Robot arm GUI
Version 1.0 - Initial Release
Sends command for each joint of robot arm.
Input is degrees, sends microsecond delay to Arduino Uno
Also has the option to write the delay in us directly, mostly used for development and calibration.
"""
import sys
# from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout
import serial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

ser = serial.Serial('COM3', 9600)


def deg2us(deg, m, b):
    [deg, m, b] = [float(i) for i in [deg, m, b]]
    us = round(deg * m + b)
    return us


class RobotGUI(QWidget):

    def __init__(self):
        super(RobotGUI, self).__init__()

        self.chk = QCheckBox('Write µs')

        self.lbl_jnt = QLabel('Joint')
        self.lbl_jnt.setAlignment(Qt.AlignCenter)
        self.lbl_ang = QLabel('Angle (deg)')
        self.lbl_ang.setAlignment(Qt.AlignCenter)

        self.lbl_j0 = QLabel('J0')
        self.sb_j0 = QDoubleSpinBox()
        self.sb_j0.setRange(5, 175)
        self.sb_j0.setValue(90.0)

        self.lbl_j1 = QLabel('J1')
        self.sb_j1 = QDoubleSpinBox()
        self.sb_j1.setRange(0, 180)
        self.sb_j1.setValue(60.0)

        self.lbl_j2 = QLabel('J2')
        self.sb_j2 = QDoubleSpinBox()
        self.sb_j2.setRange(25, 180)
        self.sb_j2.setValue(25.0)

        self.lbl_j3 = QLabel('J3')
        self.sb_j3 = QDoubleSpinBox()
        self.sb_j3.setRange(80, 250)
        self.sb_j3.setValue(110.0)

        self.lbl_j4 = QLabel('J4')
        self.sb_j4 = QDoubleSpinBox()
        self.sb_j4.setRange(0, 250)
        self.sb_j4.setValue(10.0)

        self.btn_snd = QPushButton('Send to Bot')

        self.init_ui()

    def init_ui(self):

        grid = QGridLayout()
        self.setLayout(grid)
        positions = [(i, j) for i in range(5) for j in range(4)]
        grid.addWidget(self.lbl_jnt, 0, 0)
        grid.addWidget(self.lbl_ang, 0, 1)

        grid.addWidget(self.lbl_j0, 1, 0)
        grid.addWidget(self.sb_j0, 1, 1)

        grid.addWidget(self.lbl_j1, 2, 0)
        grid.addWidget(self.sb_j1, 2, 1)

        grid.addWidget(self.lbl_j2, 3, 0)
        grid.addWidget(self.sb_j2, 3, 1)

        grid.addWidget(self.lbl_j3, 4, 0)
        grid.addWidget(self.sb_j3, 4, 1)

        grid.addWidget(self.lbl_j4, 5, 0)
        grid.addWidget(self.sb_j4, 5, 1)

        grid.addWidget(self.btn_snd,6,0,1,2)
        grid.addWidget(self.chk,0,2)

        self.btn_snd.clicked.connect(self.send_serial)
        self.chk.stateChanged.connect(self.write_us)

        self.center()
        self.setWindowTitle('Robot Arm Control')
        self.show()

    def send_serial(self):
        if self.chk.isChecked():
            cmd = str(round(self.sb_j0.value())) + 'a,' + str(round(self.sb_j1.value())) + 'b,' + str(round(self.sb_j2.value())) + 'c,' + str(round(self.sb_j3.value())) + 'd,' + str(round(self.sb_j4.value())) + 'e,;'
            ser.write(cmd.encode('utf-8'))
        else:
            us_j0 = deg2us(self.sb_j0.value(), 9.4444, 625)
            us_j1 = deg2us(self.sb_j1.value(), -9.7222, 2325)
            us_j2 = deg2us(self.sb_j2.value(), -8.0556, 2250)
            us_j3 = deg2us(self.sb_j3.value(), 10.2778, -150)
            us_j4 = deg2us(self.sb_j4.value(), 5.0000, 1050)
            cmd = str(us_j0) + 'a,' + str(us_j1) + 'b,' + str(us_j2) + 'c,' + str(us_j3) + 'd,' + str(us_j4) + 'e,;'
            ser.write(cmd.encode('utf-8'))



    def write_us(self):
        self.lbl_ang.setText('Angle (µs) ') if self.chk.isChecked() else self.lbl_ang.setText('Angle (deg)')
        self.sb_j0.setRange(500, 2500) if self.chk.isChecked() else self.sb_j0.setRange(5, 175)
        self.sb_j1.setRange(500, 2500) if self.chk.isChecked() else self.sb_j1.setRange(0, 180)
        self.sb_j2.setRange(500, 2500) if self.chk.isChecked() else self.sb_j2.setRange(25, 180)
        self.sb_j3.setRange(500, 2500) if self.chk.isChecked() else self.sb_j3.setRange(80, 250)
        self.sb_j4.setRange(500, 2500) if self.chk.isChecked() else self.sb_j4.setRange(0, 250)

        self.sb_j0.setValue(1475) if self.chk.isChecked() else self.sb_j0.setValue(90)
        self.sb_j1.setValue(1742) if self.chk.isChecked() else self.sb_j1.setValue(60)
        self.sb_j2.setValue(2049) if self.chk.isChecked() else self.sb_j2.setValue(25)
        self.sb_j3.setValue(981) if self.chk.isChecked() else self.sb_j3.setValue(110)
        self.sb_j4.setValue(1100) if self.chk.isChecked() else self.sb_j4.setValue(10)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    rg = RobotGUI()
    sys.exit(app.exec_())
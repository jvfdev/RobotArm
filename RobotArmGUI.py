"""
Robot arm GUI
Version 1.1 - Now uses R, Z, Phi, Theta to determine end effector position.
Calculates necessary robot arm joint angles
"""
import serial
import sys
import win32api

from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

ser = serial.Serial('COM3', 9600)


def deg2us(deg, m, b):
    [deg, m, b] = [float(i) for i in [deg, m, b]]
    us = round(deg * m + b)
    return us


class RobotGUI(QWidget):

    def __init__(self):
        super(RobotGUI, self).__init__()

        self.width = 545
        self.height = 200
        self.left = win32api.GetSystemMetrics(0) / 2 - self.width / 2
        self.top = win32api.GetSystemMetrics(1) / 2 - self.height / 2

        # self.chk = QCheckBox('Write µs')

        self.lbl_jnt = QLabel('End effector Position')
        self.lbl_jnt.setAlignment(Qt.AlignCenter)
        self.lbl_ang = QLabel('Angle (deg)')
        self.lbl_ang.setAlignment(Qt.AlignCenter)

        self.lbl_R = QLabel('R')
        self.sb_R = QDoubleSpinBox()
        self.sb_R.setRange(190, 300)
        self.sb_R.setValue(230.0)
        self.lbl_R_unit = QLabel('(mm)')

        self.lbl_Z = QLabel('Z')
        self.sb_Z = QDoubleSpinBox()
        self.sb_Z.setRange(0, 165)
        self.sb_Z.setValue(50.0)
        self.lbl_Z_unit = QLabel('(mm)')

        self.lbl_phi = QLabel('Phi')
        self.sb_phi = QDoubleSpinBox()
        self.sb_phi.setRange(-60, 60)
        self.sb_phi.setValue(0.0)
        self.lbl_phi_unit = QLabel('(deg)')

        self.lbl_theta = QLabel('Theta')
        self.sb_theta = QDoubleSpinBox()
        self.sb_theta.setRange(5, 175)
        self.sb_theta.setValue(90.0)
        self.lbl_theta_unit = QLabel('(deg)')

        self.lbl_grip = QLabel('Gripper')
        self.sb_grip = QDoubleSpinBox()
        self.sb_grip.setRange(0, 250)
        self.sb_grip.setValue(10.0)
        self.lbl_grip_unit = QLabel('(%)')

        self.btn_snd = QPushButton('Go to current position')

        self.init_ui()

    def init_ui(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        grid = QGridLayout()
        self.setLayout(grid)
        positions = [(i, j) for i in range(5) for j in range(4)]
        grid.addWidget(self.lbl_jnt, 0, 0, 1, 3)
        # grid.addWidget(self.lbl_ang, 0, 1)

        grid.addWidget(self.lbl_R, 1, 0)
        grid.addWidget(self.sb_R, 1, 1)
        grid.addWidget(self.lbl_R_unit, 1, 2)

        grid.addWidget(self.lbl_Z, 2, 0)
        grid.addWidget(self.sb_Z, 2, 1)
        grid.addWidget(self.lbl_Z_unit, 2, 2)

        grid.addWidget(self.lbl_phi, 3, 0)
        grid.addWidget(self.sb_phi, 3, 1)
        grid.addWidget(self.lbl_phi_unit, 3, 2)

        grid.addWidget(self.lbl_theta, 4, 0)
        grid.addWidget(self.sb_theta, 4, 1)
        grid.addWidget(self.lbl_theta_unit, 4, 2)

        grid.addWidget(self.lbl_grip, 5, 0)
        grid.addWidget(self.sb_grip, 5, 1)
        grid.addWidget(self.lbl_grip_unit, 5, 2)

        grid.addWidget(self.btn_snd,6,0,1,3)

        grid.addWidget(self.tableWidget,0,3,7,1)
        # grid.addWidget(self.chk,0,2)

        self.btn_snd.clicked.connect(self.send_serial)
        # self.chk.stateChanged.connect(self.write_us)

        # self.center()
        self.setWindowTitle('Robot Arm Control')
        self.show()

    def send_serial(self):
        # print("Send Serial Clicked")
        cmd = str(round(self.sb_R.value())) + 'R,' + str(round(self.sb_Z.value())) + 'Z,' + str(round(self.sb_phi.value())) + 'P,' + str(round(self.sb_theta.value())) + 'T,' + str(round(self.sb_grip.value())) + 'G,;'
        # print(cmd)
        ser.write(cmd.encode('utf-8'))



    # def write_us(self):
    #     self.lbl_ang.setText('Angle (µs) ') if self.chk.isChecked() else self.lbl_ang.setText('Angle (deg)')
    #     self.sb_R.setRange(500, 2500) if self.chk.isChecked() else self.sb_R.setRange(5, 175)
    #     self.sb_Z.setRange(500, 2500) if self.chk.isChecked() else self.sb_Z.setRange(0, 180)
    #     self.sb_phi.setRange(500, 2500) if self.chk.isChecked() else self.sb_phi.setRange(25, 180)
    #     self.sb_theta.setRange(500, 2500) if self.chk.isChecked() else self.sb_theta.setRange(80, 250)
    #     self.sb_grip.setRange(500, 2500) if self.chk.isChecked() else self.sb_grip.setRange(0, 250)
    #
    #     self.sb_R.setValue(1475) if self.chk.isChecked() else self.sb_R.setValue(90)
    #     self.sb_Z.setValue(1742) if self.chk.isChecked() else self.sb_Z.setValue(60)
    #     self.sb_phi.setValue(2049) if self.chk.isChecked() else self.sb_phi.setValue(25)
    #     self.sb_theta.setValue(981) if self.chk.isChecked() else self.sb_theta.setValue(110)
    #     self.sb_grip.setValue(1100) if self.chk.isChecked() else self.sb_grip.setValue(10)

    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['CMD','R', 'Z', 'Phi', 'Theta', 'Grip'])
        # self.tableWidget.setColumnWidth([0,1], [10, 10])
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i, 60)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    rg = RobotGUI()
    sys.exit(app.exec_())
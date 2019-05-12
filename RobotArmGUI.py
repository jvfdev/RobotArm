"""
Robot arm GUI
Version 1.1 - Now uses R, Z, Phi, Theta to determine end effector position.
Calculates necessary robot arm joint angles
"""
import serial
import sys
import win32api
import math
import time
import random
import ctypes

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

try:
    ser = serial.Serial('COM3', 9600)
except:
    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    Mbox('Error!', 'Error: Unable to communicate with Arduino.\
                    \nMake sure that it is plugged in and that no other programs are talking to it.\n\
The program will now exit.', 0)
    sys.exit()


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

        self.lbl_jnt = QLabel('End Effector Position')
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
        self.rcd_btn = QPushButton('Record current position')
        self.run_btn = QPushButton('Run')
        self.pse_btn = QPushButton('Add wait')
        self.lop_btn = QPushButton('Add loop')

        # define local variables
        self.r = 0
        self.z = 0
        self.phi = 0
        self.theta = 0
        self.grip = 0

        self.wait = 0
        self.num_loops = 0
        self.loop_line = 0


        self.init_ui()

    def init_ui(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_table()

        grid = QGridLayout()
        self.setLayout(grid)

        # Add current parameters UI features
        grid.addWidget(self.lbl_jnt, 0, 0, 1, 3)

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

        grid.addWidget(self.btn_snd, 6, 0, 1, 3)

        # Table features
        grid.addWidget(self.tableWidget, 0, 3, 9, 1)

        # Program manipulation UI features
        grid.addWidget(self.rcd_btn, 7, 0, 1, 3)
        grid.addWidget(self.run_btn, 9, 3)
        grid.addWidget(self.pse_btn,8,0,1,3)
        grid.addWidget(self.lop_btn, 9, 0, 1, 3)

        # Button actions
        self.btn_snd.clicked.connect(self.manual_send)
        self.rcd_btn.clicked.connect(self.record_in_table)
        self.run_btn.clicked.connect(self.run_program)
        self.pse_btn.clicked.connect(self.add_pause)
        self.lop_btn.clicked.connect(self.add_loop)

        # Window properties
        self.setWindowTitle('Robot Arm Control')
        self.show()

    def add_loop(self):
        #print("test add loop")
        loop2, ok_pressed_loop = QInputDialog.getInt(self, "Loop", "What line do you want to loop to?", 1, 1, self.tableWidget.rowCount() - 1, 1)
        if ok_pressed_loop:
            n_loops, ok_pressed_num_loops = QInputDialog.getInt(self, "Number of loops", "Enter the number of times you want to loop", 1, 1, 10000, 1)
            if ok_pressed_num_loops:
                self.num_loops = n_loops
                self.loop_line = loop2
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem('LOOP'))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(str(loop2)))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(str(n_loops)))
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

    def add_pause(self):
        #print("test pause")
        d, ok_pressed_pause = QInputDialog.getDouble(self, "Enter wait time", "Enter wait time (s) [Enter 0 for Random]:", 0, 0, 360, 1)
        if ok_pressed_pause:
            print(d)
            self.wait = d
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem('WAIT'))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(str(d)))
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

    def manual_send(self):
        self.r = self.sb_R.value()
        self.z= self.sb_Z.value()
        self.phi = self.sb_phi.value()
        self.theta = self.sb_theta.value()
        self.grip = self.sb_grip.value()
        self.send_serial()

    def send_serial(self):
        # print("Send Serial Clicked")
        # cmd = str(round(self.sb_R.value())) + 'R,'
        # + str(round(self.sb_Z.value())) + 'Z,' + str(round(self.sb_phi.value())) + 'P,'
        # + str(round(self.sb_theta.value())) + 'T,' + str(round(self.sb_grip.value())) + 'G,;'
        cmd = str(round(self.r)) + 'R,' +\
              str(round(self.z)) + 'Z,' +\
              str(round(self.phi)) + 'P,' +\
              str(round(self.theta)) + 'T,' +\
              str(round(self.grip)) + 'G,;'
        print(cmd)
        ser.write(cmd.encode('utf-8'))

    def run_program(self):
        print('Run clicked')
        #for i in range(self.tableWidget.rowCount() - 1):
        i = 0
        temp_loops = self.num_loops # restores this value after execution
        while i < self.tableWidget.rowCount() - 1:

            #rand_dwell = random.random()
            # print('test rand: ' + str(rand_dwell))
            maxloop = self.tableWidget.rowCount() - 1
            print('i: ' + str(i) + 'of' + str(maxloop))
            #print(self.tableWidget.item(i,0).text())
            if self.tableWidget.item(i,0).text() == "GOTO":
                self.r = float(self.tableWidget.item(i, 1).text())
                self.z = float(self.tableWidget.item(i, 2).text())
                self.phi = float(self.tableWidget.item(i, 3).text())
                self.theta = float(self.tableWidget.item(i, 4).text())
                self.grip = float(self.tableWidget.item(i, 5).text())
                if i > 0:
                    d = math.sqrt((self.r - r_old) ** 2 +
                              (self.z - z_old) ** 2 +
                              (self.theta - theta_old) ** 2 +
                              (self.phi - phi_old) ** 2 +
                              (self.grip - grip_old) ** 2)
                    v = 30.0
                    t = max(1.2 * d/v, 0.5)  # increases wait by 10% to allow robot to keep pace
                    # print(t)
                    time.sleep(t)
                self.send_serial()
                r_old = self.r
                z_old = self.z
                theta_old = self.theta
                phi_old = self.phi
                grip_old = self.grip

            if self.tableWidget.item(i,0).text() == "WAIT":
                print("user has become the waiter")
                self.wait = float(self.tableWidget.item(i, 1).text())
                if self.wait == 0:
                    random.seed()
                    self.wait = random.random() + 1.0
                print('sleep: ' + str(self.wait))
                time.sleep(self.wait)

            if self.tableWidget.item(i,0).text() == "LOOP":
                print("loopin'")
                if self.num_loops > 0:
                    self.num_loops = self.num_loops - 1
                    i = self.loop_line-2

            i = i+1
        self.num_loops = temp_loops
            # print('R:' + str(self.r) + ' | ')



    def record_in_table(self):
        # print(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem('GOTO'))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(self.sb_R.text()))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(self.sb_Z.text()))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(self.sb_phi.text()))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(self.sb_theta.text()))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, QTableWidgetItem(self.sb_grip.text()))
        # print(self.sb_R.text())
        # self.tableWidget.setItem(0, 1, QTableWidgetItem('new'))
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)


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

    def create_table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['CMD', 'R', 'Z', 'Phi', 'Theta', 'Grip'])
        # self.tableWidget.setColumnWidth([0,1], [10, 10])
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i, 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rg = RobotGUI()
    sys.exit(app.exec_())

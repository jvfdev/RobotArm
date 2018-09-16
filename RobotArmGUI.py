"""
Robot arm GUI
Version 0.10 - development
sends individual motor commands to Robot. Input is degrees, sends microsecond delay to Arduino Uno
"""
import sys
# from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout
import serial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

ser = serial.Serial('COM3', 9600)


def deg2us(deg, t1, t2):
    [deg,t1,t2] = [float(i) for i in [deg, t1, t2]]

    us = round(deg * ((t2 - t1) / 90.0) + t1)
    print(f_inputs)
    # us = 1
    return 0

class RobotGUI(QWidget):

    def __init__(self):
        super(RobotGUI, self).__init__()
        # self.btn = QPushButton('testbtn')

        self.onlynum = QDoubleValidator()

        self.lbl_jnt = QLabel('Joint')
        self.lbl_jnt.setAlignment(Qt.AlignCenter)
        self.lbl_ang = QLabel('Angle (degrees)')
        self.lbl_ang.setAlignment(Qt.AlignCenter)
        # self.lbl_inc = QLabel('Increase')
        # self.lbl_inc.setAlignment(Qt.AlignCenter)
        # self.lbl_dec = QLabel('Decrease')
        # self.lbl_dec.setAlignment(Qt.AlignCenter)

        self.lbl_j0 = QLabel('J0')
        self.sb_j0 = QDoubleSpinBox()
        self.sb_j0.setRange(0, 180)
        self.sb_j0.setValue(90.0)
        # self.le_j0 = QLineEdit()
        # self.le_j0.setMaxLength(5)
        # self.le_j0.setValidator(self.onlynum)
        # self.btn_j0i = QPushButton("+")
        # self.btn_j0d = QPushButton("-")

        self.lbl_j1 = QLabel('J1')
        self.sb_j1 = QDoubleSpinBox()
        self.sb_j1.setRange(0, 180)
        self.sb_j1.setValue(90.0)
        # self.le_j1 = QLineEdit()
        # self.le_j1.setMaxLength(5)
        # self.le_j1.setValidator(self.onlynum)
        # self.btn_j1i = QPushButton("+")
        # self.btn_j1d = QPushButton("-")

        self.lbl_j2 = QLabel('J2')
        self.sb_j2 = QDoubleSpinBox()
        self.sb_j2.setRange(0, 180)
        self.sb_j2.setValue(90.0)
        # self.le_j2 = QLineEdit()
        # self.le_j2.setMaxLength(5)
        # self.le_j2.setValidator(self.onlynum)
        # self.btn_j2i = QPushButton("+")
        # self.btn_j2d = QPushButton("-")

        self.lbl_j3 = QLabel('J3')
        self.sb_j3 = QDoubleSpinBox()
        self.sb_j3.setRange(0, 180)
        self.sb_j3.setValue(90.0)


        self.lbl_j4 = QLabel('J4')
        self.sb_j4 = QDoubleSpinBox()
        self.sb_j4.setRange(0, 180)
        self.sb_j4.setValue(90.0)

        self.le_fb = QLineEdit()
        self.btn_snd = QPushButton('Send to Bot')

        self.test = QDoubleSpinBox()
        self.test.setRange(10,20)
        self.test.setValue(15.0)
        # self.test.setDecimals(1)

        self.init_ui()


    def init_ui(self):

        grid = QGridLayout()
        self.setLayout(grid)
        positions = [(i, j) for i in range(5) for j in range(4)]
        grid.addWidget(self.lbl_jnt, 0, 0)
        grid.addWidget(self.lbl_ang, 0, 1)
        # grid.addWidget(self.lbl_inc, 0, 2)
        # grid.addWidget(self.lbl_dec, 0, 3)
        #
        grid.addWidget(self.lbl_j0, 1, 0)
        grid.addWidget(self.sb_j0, 1, 1)
        # grid.addWidget(self.btn_j0i, 1, 2)
        # grid.addWidget(self.btn_j0d, 1, 3)
        #
        grid.addWidget(self.lbl_j1, 2, 0)
        grid.addWidget(self.sb_j1, 2, 1)
        # grid.addWidget(self.btn_j1i, 2, 2)
        # grid.addWidget(self.btn_j1d, 2, 3)
        #
        grid.addWidget(self.lbl_j2, 3, 0)
        grid.addWidget(self.sb_j2, 3, 1)
        # grid.addWidget(self.btn_j2i, 3, 2)
        # grid.addWidget(self.btn_j2d, 3, 3)
        #
        grid.addWidget(self.lbl_j3, 4, 0)
        grid.addWidget(self.sb_j3, 4, 1)
        # grid.addWidget(self.btn_j3i, 4, 2)
        # grid.addWidget(self.btn_j3d, 4, 3)
        #
        grid.addWidget(self.lbl_j4, 5, 0)
        grid.addWidget(self.sb_j4, 5, 1)
        # grid.addWidget(self.btn_j4i, 5, 2)
        # grid.addWidget(self.btn_j4d, 5, 3)
        #
        # grid.addWidget(self.le_fb,1,4)
        #
        grid.addWidget(self.btn_snd,6,0,1,2)
        # grid.addWidget(self.test,2,4)
        # grid.setSpacing(10)


        # self.le_j0.textChanged.connect(self.txtchgj0)

        self.btn_snd.clicked.connect(self.send_serial)
        self.test.valueChanged.connect(self.send_serial)


        # row0 = QHBoxLayout()
        # row0.addWidget(self.lbl_jnt)
        # row0.addWidget(self.lbl_ang)
        # row0.addWidget(self.lbl_inc)
        # row0.addWidget(self.lbl_dec)
        #
        #
        # row1 = QHBoxLayout()()
        # row1.addWidget(self.lbl_j0)
        # row1.addWidget(self.le)
        # row1.addWidget(self.btn_j0i)
        # row1.addWidget(self.btn_j0d)
        #
        # v_box = QVBoxLayout()
        # v_box.addLayout(row0)
        # v_box.addLayout(row1)

        # self.setLayout(v_box)
        # self.resize(1280,720)
        self.center()
        self.setWindowTitle('Robot Arm Control')
        self.show()

    def send_serial(self):
        deg2us(self.sb_j0.value(), 625, 1475)
        # a = self.test.value()
        # print(a)

    def txtchgj0(self):
        pass
        # self.le_fb.setText(self.le_j0.text())
        # a = float(self.le_j0.text())

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    rg = RobotGUI()
    sys.exit(app.exec_())
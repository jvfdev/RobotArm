"""
Robot arm GUI
Version 0.10 - development
sends individual motor commands to Robot. Input is degrees, sends microsecond delay to Arduino Uno
"""
import sys
# from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RobotGUI(QWidget):

    def __init__(self):
        super(RobotGUI, self).__init__()
        # self.btn = QPushButton('testbtn')

        self.onlyint = QDoubleValidator()

        self.lbl_jnt = QLabel('Joint')
        self.lbl_jnt.setAlignment(Qt.AlignCenter)
        self.lbl_ang = QLabel('Angle (degrees)')
        self.lbl_ang.setAlignment(Qt.AlignCenter)
        self.lbl_inc = QLabel('Increase')
        self.lbl_inc.setAlignment(Qt.AlignCenter)
        self.lbl_dec = QLabel('Decrease')
        self.lbl_dec.setAlignment(Qt.AlignCenter)

        self.lbl_j0 = QLabel('J0')
        self.le_0 = QLineEdit()
        self.le_0.setMaxLength(5)
        self.le_0.setValidator(self.onlyint)
        self.btn_j0i = QPushButton("Increase")
        self.btn_j0d = QPushButton("Decrease")

        self.lbl_j1 = QLabel('J1')
        self.le_j1 = QLineEdit()
        self.le_j1.setMaxLength(5)
        self.le_j1.setValidator(self.onlyint)
        self.btn_j1i = QPushButton("Increase")
        self.btn_j1d = QPushButton("Decrease")

        self.lbl_j2 = QLabel('J2')
        self.le_j2 = QLineEdit()
        self.le_j2.setMaxLength(5)
        self.le_j2.setValidator(self.onlyint)
        self.btn_j2i = QPushButton("Increase")
        self.btn_j2d = QPushButton("Decrease")

        self.lbl_j3 = QLabel('J3')
        self.le_j3 = QLineEdit()
        self.le_j3.setMaxLength(5)
        self.le_j3.setValidator(self.onlyint)
        self.btn_j3i = QPushButton("Increase")
        self.btn_j3d = QPushButton("Decrease")

        self.lbl_j4 = QLabel('J4')
        self.le_j4 = QLineEdit()
        self.le_j4.setMaxLength(5)
        self.le_j4.setValidator(self.onlyint)
        self.btn_j4i = QPushButton("Increase")
        self.btn_j4d = QPushButton("Decrease")

        self.init_ui()


    def init_ui(self):

        grid = QGridLayout()
        self.setLayout(grid)
        positions = [(i, j) for i in range(5) for j in range(4)]
        grid.addWidget(self.lbl_jnt, 0, 0)
        grid.addWidget(self.lbl_ang, 0, 1)
        grid.addWidget(self.lbl_inc, 0, 2)
        grid.addWidget(self.lbl_dec, 0, 3)

        grid.addWidget(self.lbl_j0, 1, 0)
        grid.addWidget(self.le_0, 1, 1)
        grid.addWidget(self.btn_j0i, 1, 2)
        grid.addWidget(self.btn_j0d, 1, 3)

        grid.addWidget(self.lbl_j1, 2, 0)
        grid.addWidget(self.le_j1, 2, 1)
        grid.addWidget(self.btn_j1i, 2, 2)
        grid.addWidget(self.btn_j1d, 2, 3)

        grid.addWidget(self.lbl_j2, 3, 0)
        grid.addWidget(self.le_j2, 3, 1)
        grid.addWidget(self.btn_j2i, 3, 2)
        grid.addWidget(self.btn_j2d, 3, 3)

        grid.addWidget(self.lbl_j3, 4, 0)
        grid.addWidget(self.le_j3, 4, 1)
        grid.addWidget(self.btn_j3i, 4, 2)
        grid.addWidget(self.btn_j3d, 4, 3)

        grid.addWidget(self.lbl_j4, 5, 0)
        grid.addWidget(self.le_j4, 5, 1)
        grid.addWidget(self.btn_j4i, 5, 2)
        grid.addWidget(self.btn_j4d, 5, 3)

        # row0 = QHBoxLayout()
        # row0.addWidget(self.lbl_jnt)
        # row0.addWidget(self.lbl_ang)
        # row0.addWidget(self.lbl_inc)
        # row0.addWidget(self.lbl_dec)
        #
        #
        # row1 = QHBoxLayout()
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


    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    rg = RobotGUI()
    sys.exit(app.exec_())
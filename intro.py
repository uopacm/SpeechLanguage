import sys
import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea, QPushButton, QRadioButton, QButtonGroup, QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

import datetime
import json

class IntroScreen(QMainWindow):
    def __init__(self):
        super(IntroScreen, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.payload = []
        self.setupItems()

    def save_settings(self):
        if self.payload[2]:
            for i in range(100):
                if i < 10:
                    if not os.path.exists('{}-{}-{}-{}'.format(self.payload[0], 'A0{}'.format(str(i + 1)), self.payload[1], 'PWS')):
                        os.makedirs('{}-{}-{}-{}'.format(self.payload[0], 'A0{}'.format(str(i + 1)), self.payload[1], 'PWS'))
                        sys.exit()
                else:
                    if not os.path.exists('{}-{}-{}-{}'.format(self.payload[0], 'A{}'.format(str(i + 1)), self.payload[1], 'PWS')):
                        os.makedirs('{}-{}-{}-{}'.format(self.payload[0], 'A{}'.format(str(i + 1)), self.payload[1], 'PWS'))
                        sys.exit()
        else:
            for i in range(100):
                if i < 10:
                    if not os.path.exists('{}-{}-{}-{}'.format(self.payload[0], 'A0{}'.format(str(i + 1)), self.payload[1], 'PNS')):
                        os.makedirs('{}-{}-{}-{}'.format(self.payload[0], 'A0{}'.format(str(i + 1)), self.payload[1], 'PNS'))
                        sys.exit()
                else:
                    if not os.path.exists('{}-{}-{}-{}'.format(self.payload[0], 'A{}'.format(str(i + 1)), self.payload[1], 'PNS')):
                        os.makedirs('{}-{}-{}-{}'.format(self.payload[0], 'A{}'.format(str(i + 1)), self.payload[1], 'PNS'))
                        sys.exit()

    def setupItems(self):
        m = datetime.datetime.today().month
        ms = ''
        d = datetime.datetime.today().day
        ds = ''

        if m < 10:
            ms += '0'
        ms += str(m)
        if d < 10:
            ds += '0'
        ds += str(d)
        ys = str(datetime.datetime.today().year)

        self.w = QWidget(self)
        self.l = QHBoxLayout(self.w)

        self.payload.append('{}{}{}'.format(ms, ds, ys[2:]))

        self.gender = QButtonGroup(self.w)

        self.male = QRadioButton('Male')
        self.male.toggled.connect(lambda:self.chngstate_gender(self.male))
        self.male.move(10, 10)
        self.gender.addButton(self.male)

        self.female = QRadioButton('Female')
        self.female.toggled.connect(lambda:self.chngstate_gender(self.female))
        self.female.move(60, 10)
        self.gender.addButton(self.female)

        self.payload.append('')

        self.stutters = QButtonGroup(self.w)

        self.stutter = QRadioButton('I have a stutter.')
        self.stutter.toggled.connect(lambda:self.chngstate_stutter(self.stutter))
        self.stutter.move(10, 50)
        self.stutters.addButton(self.stutter)

        self.nostutter = QRadioButton('I don\'t have a stutter.')
        self.nostutter.toggled.connect(lambda:self.chngstate_stutter(self.nostutter))
        self.nostutter.move(150, 50)
        self.stutters.addButton(self.nostutter)

        self.payload.append(False)

        self.l.addWidget(self.male)
        self.l.addWidget(self.female)
        self.l.addWidget(self.stutter)
        self.l.addWidget(self.nostutter)

        self.setCentralWidget(self.w)

        self.btn = QPushButton('Continue', self)
        self.btn.clicked.connect(self.save_settings)
        self.btn.resize(self.btn.minimumSizeHint())
        self.btn.move(10, 100)

        self.show()

    def chngstate_gender(self, btn):
        if btn.text() == 'Male':
            if btn.isChecked():
                self.payload[1] = 'M'
        elif btn.text() == 'Female':
            if btn.isChecked():
                self.payload[1] = 'F'

    def chngstate_stutter(self, btn):
        if btn.text() == 'I have a stutter.':
            if btn.isChecked():
                self.payload[2] = True
        elif btn.text() == 'I don\'t have a stutter.':
            if btn.isChecked():
                self.payload[2] = False

def run():
    app = QApplication(sys.argv)
    GUI = IntroScreen()
    sys.exit(app.exec_())
    return GUI.payload

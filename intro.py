import sys
import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea, QPushButton, QRadioButton, QButtonGroup, QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

import datetime
import json

class IntroScreen(QWidget):
    def __init__(self, parent):
        super(IntroScreen, self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.payload = []
        self.setupItems()
        self.subject_id = ''
        self.setStyleSheet("""
        .QWidget {
            border-radius: 8px;
            background-color: lightgrey;
            }
        """)

    def subject_file_name(self, i, style, condition):
        """ Returns a formatted subject name. Eg. 043017-A01-M-PWS """
        return '{}-{}-{}-{}'.format(self.payload[0],
                                    style.format(str(i + 1)),
                                    self.payload[1],
                                    condition)
    
    def next_subject_num(self, style, condition, start, end):
        """ Checks the file system for the next available subject number. """
        return next((x for x in range(start, end)
                     if not os.path.exists(self.subject_file_name(x, style, condition)))
                    , None)
        
    def create_subject_id_and_folder(self):
        condition = 'PWS' if self.payload[2] else 'PNS'
        style = 'A0{}'
        subject_num = self.next_subject_num(style, condition, 0, 10)
        
        if subject_num is None:
            style = 'A{}'
            subject_num = self.next_subject_num(style, condition, 10, 100)

        self.subject_id = self.subject_file_name(subject_num, style, condition)
        os.makedirs(self.subject_id)

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
    #GUI = IntroScreen()
    sys.exit(app.exec_())
    #return GUI.payload

if __name__ == "__main__":
    run()

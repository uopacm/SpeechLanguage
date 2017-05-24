import sys
import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea, QPushButton, QRadioButton, QButtonGroup, QWidget, QHBoxLayout, QSpinBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

import datetime
import json

class IntroScreen(QWidget):
    def __init__(self, parent):
        super(IntroScreen, self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.payload = []
        self.subject_info = ''
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
        return '{}-{}-{}-{}-{}'.format(self.payload[0],
                                    style.format(str(i)),
                                    self.payload[1],
                                    self.age.value(),
                                    condition)
    
        
    def create_subject_id_and_folder(self):
        condition = 'PWS' if self.payload[2] else 'PNS'
        style = self.payload[6] + '0{}' if self.participant.value() < 10 else self.payload[6] + '{}'
        self.subject_info = ( self.payload[0] + ", "
                            + str(self.age.value()) + ", "
                            + str(self.payload[1]) + ", "
                            + condition + ", "
                            + self.payload[6] + ", "
                            + str(self.participant.value()) + ", ")
        
        self.subject_id = self.subject_file_name(self.participant.value(), style, condition)
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

        self.age_label = QLabel(self)
        self.age_label.setText("age")
        self.age_label.move(145,50)
        self.age = QSpinBox(self)
        self.age.move(170,50)

        self.experimenter = QButtonGroup(self.w)

        self.experimenter_buttons = []

        def select_experimenter(letter):
            def select():
                self.payload[6] = letter
            return select

        distance = 0
        for letter in ['A','B','C','D']:
            radio = QRadioButton(letter)
            radio.toggled.connect(select_experimenter(letter))
            radio.move(170 + distance,70)
            distance += 20
            self.experimenter.addButton(radio)
            self.experimenter_buttons.append(radio)


        self.participant_label = QLabel(self)
        self.participant_label.setText("participant")
        self.participant_label.move(110,70)
        self.participant = QSpinBox(self)
        self.participant.move(170,70)
        
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
        self.payload.extend([0,0,0,0])

        self.l.addWidget(self.male)
        self.l.addWidget(self.female)
        self.l.addWidget(self.stutter)
        self.l.addWidget(self.nostutter)
        for e in self.experimenter_buttons:
            self.l.addWidget(e)

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

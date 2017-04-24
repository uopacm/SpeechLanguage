import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

import random

from recordSound import AudioRecorder

import queue
from study import *



# Skeleton source from online
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isRecording = False
        self.left = 500
        self.top = 300
        self.windowWidth = 700
        self.windowHeight = 500

        self.initUI()

        # Setup everything for audio recording
        self.audio_recorder = AudioRecorder()

        # Holds a Queue of the different page contents
        self.content = {}

        # Holds the info for the current page
        self.current_page = {}
        
        # Have run() handle all methods
        self.run()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.windowWidth, self.windowHeight)
        self.setWindowTitle('Main Menu')

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # Not quite sure about the differences between all the layout options....
        self.layout = QGridLayout()

        self.scroll_area = QScrollArea(self)
        
        # Widgets used for application
        self.spacePressed = QLabel("Record on.", self)

        self.spaceNotPressed = QLabel("Record off.", self)
        self.phrase = QLabel(self)
        self.title = QLabel(self)
        self.font = QtGui.QFont()

        # Add widgets to layout
        self.layout.addWidget(self.title)
        self.scroll_area.setWidget(self.phrase)
        self.layout.addWidget(self.scroll_area)
        
        # Hide all widgets for now
        self.phrase.hide()
        self.spacePressed.hide()
        self.spaceNotPressed.hide()

        self.show()

    def run(self):

        # Get subject id
        # self.get_subect_info()
        subject_info = "subejct1"
        self.content = setup_study(subject_info)
        self.next_page()
        self.showPhrases()
        self.showTitle()

    def showLabel(self, label):
        # Edit phrase
        self.font.setPointSize(12)
        label.setWordWrap(True)
        label.setFont(self.font)
        label.setAlignment(Qt.AlignCenter)
        label.adjustSize()
        self.spacePressed.move(self.width()/2, self.height()/2)
                              
    def showTitle(self):
        self.showLabel(self.title)
        self.title.move(self.width()/4, self.height()/4)
        self.title.show()
        
    def showPhrases(self):
        # Read in first paragraph of phrases.txt
        # text = open('phrases.txt').read().splitlines()
        # line = random.choice(text) # Choose random line
        self.showLabel(self.phrase)
        self.phrase.move(self.width()/4, self.height()/2)
        self.scroll_area.adjustSize()
        self.scroll_area.move(self.width()/4, self.height()/2)
        self.scroll_area.setWidgetResizable(True)
        self.phrase.show()

    def next_page(self):
        self.current_page = self.content.pop(0)

        if(self.current_page is None):
            # Exit the program
            pass
        elif(type(self.current_page) is TextWindow):
            self.title.show()
            self.title.setText(self.current_page.header)
            self.phrase.setText(self.current_page.text)
        elif(type(self.current_page) is BaseRecording):
            self.title.hide()
            self.phrase.setText(self.current_page.text)
        
    def base_recording_window_spacebar(self, event):
        if event.key() == Qt.Key_Space and self.isRecording == False:
            self.isRecording = True
            self.audio_recorder.start_recording("test.wav")
            self.title.setText("Recording on.")
            self.title.show()
        elif (event.key() == Qt.Key_Space and self.isRecording):
            self.isRecording = False
            self.audio_recorder.stop_recording()
            self.title.setText("Recording off.")
            self.title.show()
        
    def keyPressEvent(self, event):

        if (type(self.current_page) is TextWindow):
            self.next_page()
        elif(type(self.current_page) is BaseRecording):
            self.base_recording_window_spacebar(event)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

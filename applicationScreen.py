import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

import random

from recordSound import AudioRecorder

from study import *
import waveform

from QRoundProgressBar import *

WAV_IMAGE_HEIGHT = 500
WAV_IMAGE_WIDTH = 1000



# Skeleton source from online
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 300
        self.windowWidth = 1720
        self.windowHeight = 1000

        self.initUI()

        # Setup everything for audio recording
        self.audio_recorder = AudioRecorder()

        # Holds a Queue of the different page contents
        self.content = {}

        # Sequences the actions for the space bar
        self.spacebar_actions = []

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
        self.phrase = QLabel(self)
        self.title = QLabel(self)
        self.font = QtGui.QFont()
        self.pacman = QRoundProgressBar(self)

        # Image for the wav form trimming
        self.wav_image = QLabel(self)
        self.wav_image.resize(WAV_IMAGE_WIDTH,WAV_IMAGE_HEIGHT)

        # Add widgets to layout
        self.layout.addWidget(self.title)
        self.scroll_area.setWidget(self.phrase)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.wav_image)
        self.layout.addWidget(self.pacman)
        
        # Hide all widgets for now
        self.phrase.hide()
        self.wav_image.hide()

        self.show()
        self.pacman.show()

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

    
    def recording_on(self):
            self.audio_recorder.start_recording(self.current_page.output_file)
            self.title.setText("Recording on.")
            self.title.show()

    def recording_off(self):
            self.audio_recorder.stop_recording()
            self.title.setText("Recording off.")
            self.title.show()        

    def next_page(self):
        self.spacebar_actions = []
        self.current_page = self.content.pop(0)

        if(self.current_page is None):
            # Exit the program
            pass

        # ------ Setup a Text  Window Page --------
        elif(type(self.current_page) is TextWindow):
            self.title.show()
            self.title.setText(self.current_page.header)
            self.phrase.setText(self.current_page.text)

        # ------ Setup a Base Recording Page ---------
        elif(type(self.current_page) is BaseRecording):
            self.title.hide()
            self.phrase.setText(self.current_page.text)

            # Spacebar actions for Base Recording
            self.spacebar_actions.append(self.recording_on)
            self.spacebar_actions.append(self.recording_off)
            
        elif(type(self.current_page) is TrimAudio):
            waveform.generatePng(self.current_page.wav_file)
            image = QPixmap(self.current_page.wav_file + '.png')
            self.wav_image.setPixmap(image.scaled(WAV_IMAGE_WIDTH, WAV_IMAGE_HEIGHT))
            self.wav_image.show()
                
            
    def keyPressEvent(self, event):
        if not self.spacebar_actions:
            self.next_page()
        else:
            action = self.spacebar_actions.pop(0)
            action()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

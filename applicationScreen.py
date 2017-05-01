import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMessageBox, QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5 import Qt

import random

from recordSound import AudioRecorder

from study import *
import waveform

from QRoundProgressBar import *

WAV_IMAGE_HEIGHT = 500
WAV_IMAGE_WIDTH = 1000
from intro import IntroScreen


class MyEventFilter(QObject):
    def __init__(self, top_level):
        super().__init__()
        self.app = top_level
        
    def eventFilter(self, receiver, event):
        if(event.type() == QEvent.KeyPress):
            self.app.keyPressEvent(event)
            return True
        else:      
            #Call Base Class Method to Continue Normal Event Processing
            return super(MyEventFilter,self).eventFilter(receiver, event)

# Skeleton source from online
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 300
        self.windowWidth = 1000
        self.windowHeight = 800
        self.font = QtGui.QFont()
        
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

        # IntroScreen
        self.intro_screen = IntroScreen(self)
        self.layout.addWidget(self.intro_screen)
        self.center(self.intro_screen)
        self.intro_screen.setFixedWidth(500)
        self.intro_screen.setFixedHeight(300)
        self.intro_screen.show()
        
        # Pacman Progress Bar
        self.pacman = QRoundProgressBar(self)
        self.pacman.setBarStyle(2) # Pie
        self.pacman.setFixedWidth(200)
        self.pacman.setFixedHeight(200)
        self.center(self.pacman)
        self.pacman.lower()
        self.pacman.setWindowOpacity(0.9)
        self.layout.addWidget(self.pacman)
        self.pacman.hide()
        
        # Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.move(self.width()/4, self.height()/4)
        self.scroll_area.setFixedWidth(700)
        self.scroll_area.setFixedHeight(500)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.hide()

        # Scrolling Text
        self.scroll_text = QLabel(self)
        self.showLabel(self.scroll_text)
        self.layout.addWidget(self.scroll_text)
        self.scroll_area.setWidget(self.scroll_text)
        self.scroll_text.adjustSize()
        self.scroll_text.hide()
        
        self.phrase = QLabel(self)
        self.showLabel(self.phrase)
        self.phrase.move(self.width()/4, self.height()/4)
        self.phrase.setFixedHeight(500)
        self.phrase.setFixedWidth(500)
        self.layout.addWidget(self.phrase)
        self.phrase.hide()

        self.title = QLabel(self)
        self.title.move(self.width()/4, self.height()/8)
        self.title.setFixedHeight(100)
        self.title.setFixedWidth(300)
        self.layout.addWidget(self.title)
        self.title.hide()
        
        # Image for the wav form trimming
        self.wav_image = QLabel(self)
        self.wav_image.resize(WAV_IMAGE_WIDTH,WAV_IMAGE_HEIGHT)
        self.layout.addWidget(self.wav_image)
        self.wav_image.hide()
        
        # Hide all widgets for now
        self.show()
        

    def run(self):

        # Get subject id
        # self.get_subect_info()
        subject_info = "subejct1"
        self.content = setup_study(subject_info)
        self.next_page()

    def showLabel(self, label):
        # Edit phrase
        self.font.setPointSize(12)
        label.setWordWrap(True)
        label.setFont(self.font)
        label.setAlignment(Qt.AlignCenter)
        label.adjustSize()

                              
    def showTitle(self):
        self.showLabel(self.title)
        self.title.move(self.width()/2, self.height()/2)
        self.title.show()

    def center(self, w):
        w.move(self.width()/4, self.height()/4)
    
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

        if(type(self.current_page) is Intro):
            self.intro_screen.show()
            self.title.hide()
            self.phrase.hide()
            self.spacebar_actions.append(self.intro_screen.create_subject_id_and_folder)
        
        # ------ Setup a Text  Window Page --------
        elif(type(self.current_page) is TextWindow):
            self.intro_screen.hide()
            self.title.show()
            self.title.setText(self.current_page.header)
            self.phrase.show()
            self.phrase.setText(self.current_page.text)

        # ------ Setup a Base Recording Page ---------
        elif(type(self.current_page) is BaseRecording):
            self.phrase.hide()
            self.title.show()
            self.title.setText('Press space to begin recording')
            self.scroll_text.show()
            self.scroll_text.setText(self.current_page.text)
            self.scroll_text.adjustSize()
            self.scroll_area.show()


            # Spacebar actions for Base Recording
            self.spacebar_actions.append(self.recording_on)
            self.spacebar_actions.append(self.recording_off)
            
        elif(type(self.current_page) is TrimAudio):
            waveform.generatePng(self.current_page.wav_file)
            image = QPixmap(self.current_page.wav_file + '.png')
            self.wav_image.setPixmap(image.scaled(WAV_IMAGE_WIDTH, WAV_IMAGE_HEIGHT))
            self.wav_image.show()
                
            
    def keyPressEvent(self, event):
        print(str(event.key()) + ' ' + str(Qt.Key_Space))
        if event.key() == Qt.Key_Space:
            print("press")
            if not self.spacebar_actions:
                self.next_page()
            else:
                
                action = self.spacebar_actions.pop(0)
                action()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    f = MyEventFilter(ex)
    app.installEventFilter(f)
    sys.exit(app.exec_())

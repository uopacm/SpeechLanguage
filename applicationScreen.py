import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMessageBox, QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea, QSlider
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5 import Qt

import random

from recordSound import AudioRecorder

from study import *
import waveform

from QRoundProgressBar import *
from QTimedText import *
from questionnaire import Questionnaire

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
        self.current_page = Intro()
        self.spacebar_actions.append(self.intro_complete)

        self.timer = QTimer()
        
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
        self.intro_screen.setFixedWidth(500)
        self.intro_screen.setFixedHeight(300)
        self.intro_screen.move(self.width()/4, self.height()/4)
        self.intro_screen.show()
        
        # Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.move(self.width()/4, self.height()/4)
        self.scroll_area.setFixedWidth(700)
        self.scroll_area.setFixedHeight(500)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.scroll_area)

        # Timed Text
        self.timed_text = QTimedText(self)
        self.timed_text.setFixedWidth(500)
        self.timed_text.setFixedHeight(600)
        self.timed_text.move(self.width() * 0.25, self.height() * 0.25)
        self.showLabel(self.timed_text.scroll_text)
        self.layout.addWidget(self.timed_text)

        # Normal Phrase
        self.phrase = QLabel(self)
        self.showLabel(self.phrase)
        self.phrase.move(self.width()/4, self.height()/4)
#        self.phrase.setFixedHeight(500)
#        self.phrase.setFixedWidth(500)
        self.layout.addWidget(self.phrase)
        self.scroll_area.setWidget(self.phrase)

        # Page Titles
        self.title = QLabel(self)
        self.title.move(self.width()/4, self.height()/8)
        self.title.setFixedHeight(100)
        self.title.setFixedWidth(300)
        self.layout.addWidget(self.title)
        
        # Image for the wav form trimming
        self.wav_image = QLabel(self)
        self.wav_image.resize(WAV_IMAGE_WIDTH,WAV_IMAGE_HEIGHT)
        self.layout.addWidget(self.wav_image)

        # Questionnaire
        self.questionnaire = Questionnaire(self)
        self.questionnaire.move(self.width()/4, self.height()/4)
        self.layout.addWidget(self.questionnaire)

        # Trim Audio Sliders
        self.begin_slider = QSlider(Qt.Horizontal,self)
        self.begin_slider.move(self.width() * 0.125, self.height() * 0.6)
        self.begin_slider.setFixedWidth(750)
        self.layout.addWidget(self.begin_slider)
        
        self.end_slider = QSlider(Qt.Horizontal, self)
        self.end_slider.move(self.width() * 0.125, self.height() * 0.7)
        self.end_slider.setFixedWidth(750)
        self.layout.addWidget(self.end_slider)
        
        
        self.show()
        

    def run(self):

        # Get subject id
        # self.get_subect_info()
        self.hide_all()
        self.intro_screen.show()

    def showLabel(self, label):
        # Edit phrase
        self.font.setPointSize(12)
        label.setWordWrap(True)
        label.setFont(self.font)
        label.setAlignment(Qt.AlignCenter)
        label.adjustSize()

    def hide_all(self):
        self.timed_text.hide()
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().hide()
                              
    
    def recording_on(self):
            self.audio_recorder.start_recording(self.current_page.output_file)
            self.title.setText("Recording on.")
            self.title.show()

    def recording_off(self):
            self.audio_recorder.stop_recording()
            self.title.setText("Recording off.")
            self.title.show()        

    def timer_tick(self):
        self.timed_text.pacman.setValue(self.timed_text.pacman.value + 1)

    def intro_complete(self):
        self.intro_screen.create_subject_id_and_folder()
        self.content = setup_study(self.intro_screen.subject_id)
        self.next_page()
            
    def next_page(self):
        self.spacebar_actions = []
        self.current_page = self.content.pop(0)

        # Just hide everything so each page doesn't have
        # to worry about what was already being dispalyed
        self.hide_all()
        
        if(self.current_page is None):
            # Exit the program
            pass            
        
        # ------ Setup a Text  Window Page --------
        elif(type(self.current_page) is TextWindow):
            self.title.show()
            self.title.setText(self.current_page.header)
            self.phrase.show()
            self.phrase.setText(self.current_page.text)
            self.phrase.adjustSize()
            self.scroll_area.show()

        # ------ Setup a Base Recording Page ---------
        elif(type(self.current_page) is BaseRecording):
            self.title.show()
            self.title.setText('Press space to begin recording')
            self.scroll_area.show()
            self.phrase.show()
            self.phrase.setText(self.current_page.text)
            self.phrase.adjustSize()

            # Spacebar actions for Base Recording
            self.spacebar_actions.append(self.recording_on)
            self.spacebar_actions.append(self.recording_off)

        elif(type(self.current_page) is TimedRecording):
            self.title.show()
            self.title.setText('Press space to begin recording')
            self.timed_text.setText(self.current_page.text)
            self.showLabel(self.timed_text.scroll_text)
            self.timed_text.show()
            self.timer.timeout.connect(self.timer_tick)
            self.timer.start(1000)


            # Spacebar actions for Base Recording
            self.spacebar_actions.append(self.recording_on)
            self.spacebar_actions.append(self.recording_off)
            
        elif(type(self.current_page) is TrimAudio):
            waveform.generatePng(self.current_page.wav_file)
            image = QPixmap(self.current_page.wav_file + '.png')
            self.wav_image.setPixmap(image.scaled(WAV_IMAGE_WIDTH, WAV_IMAGE_HEIGHT))
            self.wav_image.show()
            self.begin_slider.show()
            self.end_slider.show()

        elif(type(self.current_page) is Survey):
            self.questionnaire.show()
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
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

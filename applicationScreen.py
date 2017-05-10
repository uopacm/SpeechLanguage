import sys
import wave
import contextlib
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMessageBox, QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea, QSlider, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5 import Qt

import random

from recordSound import AudioRecorder
from AudioPlayback import *

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

class DataPoint():
    def __init__(self):
        self.passage = ''
        self.time = 0
        self.survey_results = []
        self.target_file = ''
        self.is_base = True
        self.percentage = 0.0

    def __str__(self):
        result = self.passage + ', ' + str(self.time) + ', '
        if  not self.is_base:
            result += str(self.percentage) + ', '
        for question in self.survey_results:
            result += str(question) + ', '
        return result

# Skeleton source from online
class App(QMainWindow):

    AUDIO_TRIM = 1000
    
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
        self.audio_playback = AudioPlayback()

        # Holds a Queue of the different page contents
        self.content = {}

        # Sequences the actions for the space bar
        self.spacebar_actions = []
        self.enter_actions = []

        self.subject_id = ''
        self.data_result = DataPoint()
    
        # Holds the info for the current page
        self.current_page = Intro()
        self.enter_actions.append(self.intro_complete)

        self.timer = QTimer()
        self.cutoff_timer = QTimer()
        self.time_limit = 0.0
        self.base_recording_times = {
            'piper' : 5000.0,
            'seashells' : 5000.0,
            'woodchuck' : 5000.0,
            'tutor' : 5000.0,
            'oyster' : 5000.0,
            'perkins' : 5000.0,
            'moses' : 5000.0,
            'blackbear' : 5000.0,
            'chester' : 5000.0,
            'betty' : 5000.0,
            '1' : 5000.0,
            '2' : 5000.0,
            '3' : 5000.0,
            '4' : 5000.0,
            '5' : 5000.0,
            '6' : 5000.0,
            '7' : 5000.0,
            '8' : 5000.0,
            '9' : 5000.0,
            '10' : 5000.0
        }
        
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
        self.intro_screen.move(self.width()/2-self.intro_screen.width()/2, self.height()/4)
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

        self.footer = QLabel(self)
        self.footer.setFixedHeight(30)
        self.footer.setFixedWidth(300)
        self.footer.move(
            self.width()/2-self.footer.width()/2, 
            (self.height() * 0.9) if (self.height() * 0.9 + self.footer.height() < self.height()) else (self.height() - self.footer.height())
        )
        self.layout.addWidget(self.footer)
        self.footer.setStyleSheet("""
        .QLabel {
            border-radius: 8px;
            background-color: lightgrey;
            padding: 2px;
            }
        """)

        
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
        self.begin_slider.setRange(0,self.AUDIO_TRIM)
        self.layout.addWidget(self.begin_slider)
        
        self.end_slider = QSlider(Qt.Horizontal, self)
        self.end_slider.move(self.width() * 0.125, self.height() * 0.7)
        self.end_slider.setFixedWidth(750)
        self.end_slider.setRange(0,self.AUDIO_TRIM)
        self.layout.addWidget(self.end_slider)

        # Trim audio playback buttons
        self.trim_audio_begin_button = QPushButton('Play', self)
        self.trim_audio_begin_button.move(0, self.height() * 0.6)
        self.trim_audio_begin_button.clicked.connect(self.playback_on(self.begin_slider))
        
        self.trim_audio_end_button = QPushButton('Play', self)
        self.trim_audio_end_button.clicked.connect(self.playback_on(self.end_slider))
        self.trim_audio_end_button.move(0, self.height() * 0.7)
        
        
        self.show()
        

    def run(self):

        # Get subject id
        # self.get_subect_info()
        self.hide_all()
        self.intro_screen.show()
        self.footer.setText('Press ENTER to continue')
        self.footer.show()

    def showLabel(self, label):
        # Edit phrase
        self.font.setPointSize(12)
        label.setWordWrap(True)
        label.setFont(self.font)
        label.setAlignment(Qt.AlignCenter)
        label.adjustSize()

    def hide_all(self):
        self.timed_text.hide()
        self.trim_audio_begin_button.hide()
        self.trim_audio_end_button.hide()
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().hide()
                              
    
    def recording_on(self):
        self.audio_recorder.start_recording(self.current_page.output_file)
        self.title.setText("Recording on.")
        self.title.show()
        self.footer.setText('Press SPACE to stop recording')
        self.footer.show()

    def recording_off(self):
        self.audio_recorder.stop_recording()
        self.cutoff_timer.stop() # Just in case the timed recording is stopped early
        self.title.setText("Recording off.")
        self.title.show()
        self.footer.setText('Press ENTER to continue')
        self.footer.show()

    def playback_on(self, slider):
        def play_from():
            duration = 0
            audio_file = self.current_page.wav_file + '.wav'

            start = (slider.value())/float(self.AUDIO_TRIM) if slider.value() != 0 else 0
            print(str(start))
            self.audio_playback.play(audio_file, start)
            self.footer.setText('Press SPACE to stop playback')
            self.spacebar_actions.append(self.playback_off)
        return play_from

    def playback_off(self):
        self.audio_playback.stop()
        self.footer.setText('Press ENTER to complete trimming')
        
    def timer_tick(self, time_limit):
        def tick():
            interval = 100.0 / time_limit
            self.timed_text.pacman.setValue(self.timed_text.pacman.value + interval)
        return tick

    def intro_complete(self):
        self.intro_screen.create_subject_id_and_folder()
        self.content = setup_study(self.intro_screen.subject_id)
        self.next_page()

    def set_trimed_audio_time(self):
        start = self.begin_slider.value()/float(self.AUDIO_TRIM)
        end = self.end_slider.value() / float(self.AUDIO_TRIM )
        with contextlib.closing(wave.open(self.current_page.wav_file + ".wav", 'r')) as r:
            frames = r.getnframes()
            rate = r.getframerate()
            duration = frames / float(rate)
            print (str(end) + ' ' + str(start))
            self.base_recording_times[self.current_page.passage] = (duration * end) - (duration * start)
            self.data_result.time = (duration * end) - (duration * start)

    def record_timed_data(self):
        with contextlib.closing(wave.open(self.current_page.output_file, 'r')) as r:
            frames = r.getnframes()
            rate = r.getframerate()
            duration = frames / float(rate)
            self.data_result.time = duration
    
    def record_passage_name(self, name):
        self.data_result.passage = name
    
    def record_survey_response(self):
        responses = []

        # Do some kind of check to make sure that all the options are selected
        
        for question in self.questionnaire.button_group_questions:
            i = 1
            for button in question.buttons():
                if button.isChecked():
                    responses.append(i)
                else:
                    i += 1
                
                
            question.setExclusive(False)
            for button in question.buttons():
                button.setChecked(False)
            question.setExclusive(True)

        self.data_result.survey_results = responses
                
    def record_data_point(self):
        with open(self.data_result.target_file, 'a+') as output:
            output.write(str(self.data_result) + '\n')
    
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
            self.title.adjustSize()
            self.phrase.show()
            self.phrase.setText(self.current_page.text)
            self.phrase.adjustSize()
            self.scroll_area.show()
            self.footer.setText('Press ENTER to continue')
            self.footer.show()

        # ------ Setup a Base Recording Page ---------
        elif(type(self.current_page) is BaseRecording):
            self.title.show()
            self.title.setText('Press space to begin recording')
            self.scroll_area.show()
            self.phrase.show()
            self.phrase.setText(self.current_page.text)
            self.phrase.adjustSize()
            self.footer.setText('Press SPACE to begin recording')
            self.footer.show()
            self.data_result.target_file = self.intro_screen.subject_id + '/' + self.intro_screen.subject_id + '-base.txt'
            self.record_passage_name(self.current_page.passage)
            self.data_result.is_base = True

            # Spacebar actions for Base Recording
            self.spacebar_actions.append(self.recording_on)
            self.spacebar_actions.append(self.recording_off)

        elif(type(self.current_page) is TimedRecording):
            self.title.show()
            self.title.setText('Press space to begin recording')
            self.timed_text.setText(self.current_page.text)
            self.timed_text.pacman.value = 0
            self.showLabel(self.timed_text.scroll_text)
            self.timed_text.show()
            self.footer.setText('Press SPACE to begin recording')
            self.footer.show()
            self.data_result.target_file = self.intro_screen.subject_id + '/' + self.intro_screen.subject_id + '-timed.txt'
            self.data_result.is_base = False
            self.data_result.percentage = self.current_page.percentage
            
            base_time = self.base_recording_times[self.current_page.passage]
            record_time = base_time * self.current_page.percentage
            self.timer.timeout.connect(self.timer_tick(record_time))
            self.cutoff_timer.timeout.connect(self.recording_off)
            self.cutoff_timer.setSingleShot(True) # Event only fires after time elapses
            print(str(record_time))
            self.cutoff_timer.start(record_time)
            self.timer.start(1) # Update the pacman every msec

            self.recording_on()
            self.footer.setText('Press SPACE to stop recording')
            self.footer.show()
            self.record_passage_name(self.current_page.passage)

            # Spacebar actions for Base Recording
            self.spacebar_actions.append(self.recording_off)
            self.enter_actions.append(self.record_timed_data)

            
        elif(type(self.current_page) is TrimAudio):
            waveform.generatePng(self.current_page.wav_file)
            image = QPixmap(self.current_page.wav_file + '.png')
            self.wav_image.setPixmap(image.scaled(WAV_IMAGE_WIDTH, WAV_IMAGE_HEIGHT))
            self.wav_image.show()
            self.begin_slider.show()
            self.trim_audio_begin_button.show()
            self.end_slider.show()
            self.trim_audio_end_button.show()
            self.footer.setText('Press ENTER to continue')
            self.footer.show()

            self.enter_actions.append(self.set_trimed_audio_time)
            self.enter_actions.append(self.record_data_point)

        elif(type(self.current_page) is Survey):
            self.questionnaire.show()
            self.footer.setText('Are you ready for the next one? Press ENTER to continue.')
            self.footer.show()
            self.enter_actions.append(self.record_survey_response)

            if not self.data_result.is_base:
                self.enter_actions.append(self.record_data_point)
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if not self.enter_actions and not self.spacebar_actions:
                self.next_page()
            elif not self.enter_actions:
                pass
            else:
                self.enter_actions.pop(0)()
        elif event.key() == Qt.Key_Space:
            if len(self.spacebar_actions) > 0:
                self.spacebar_actions.pop(0)()
                

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    f = MyEventFilter(ex)
    app.installEventFilter(f)
    sys.exit(app.exec_())

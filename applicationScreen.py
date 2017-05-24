import sys
import wave
import contextlib
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMessageBox, QMainWindow, QAction, qApp, QApplication, QLabel, QGridLayout, QScrollArea, QSlider, QPushButton, QSpinBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QFont, QIntValidator
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

WAV_IMAGE_HEIGHT = 490
WAV_IMAGE_WIDTH = 832
from intro import IntroScreen


class MyEventFilter(QObject):
    def __init__(self, top_level):
        super().__init__()
        self.app = top_level
        
    def eventFilter(self, receiver, event):
        if(event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Return or event.key() == Qt.Key_Space)):
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
        self.subject_id = ' '

    def __str__(self):
        result = self.passage + ', ' + str(round(self.time, 2)) + ', '
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
        self.windowWidth = 1200
        self.windowHeight = 800
        self.font = QtGui.QFont()
        
        self.initUI()

        # Setup everything for audio recording
        self.audio_recorder = AudioRecorder()
        self.audio_playback = AudioPlayback()

        # Holds a Queue of the different page contents
        self.experiment_start = [TextWindow(" ", "Reading Fluency with Time Pressure Study", "To begin study, please press RETURN"), Intro()]
        self.content = []
        self.content.extend(self.experiment_start)

        # Sequences the actions for the space bar
        self.spacebar_actions = []
        self.enter_actions = []

        self.subject_id = ''
        self.data_result = DataPoint()
    
        self.timer = QTimer()
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
        self.intro_screen.move(self.width() * 0.35, self.height()/2)
        self.intro_screen.show()
        
        # Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.move(self.width()/4, self.height()/4)
        self.scroll_area.setFixedWidth(740)
        self.scroll_area.setFixedHeight(500)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.scroll_area)

        # Timed Text
        self.timed_text = QTimedText(self)
        self.timed_text.setFixedWidth(740)
        self.timed_text.setFixedHeight(500)
        self.timed_text.move(self.width() * 0.25, self.height() * 0.25)
        self.showLabel(self.timed_text.scroll_text)
        self.layout.addWidget(self.timed_text)

        # Normal Phrase
        self.phrase = QLabel(self)
        self.phrase.setFont(QFont('Helvetica',16))
        self.showLabel(self.phrase)
        self.phrase.move(self.width()/4, self.height()/4)
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
        self.wav_image.move(self.width() * 0.100, 0)
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
        self.begin_slider.valueChanged.connect(self.call_update)
        self.layout.addWidget(self.begin_slider)
        
        self.end_slider = QSlider(Qt.Horizontal, self)
        self.end_slider.move(self.width() * 0.125, self.height() * 0.7)
        self.end_slider.setFixedWidth(750)
        self.end_slider.setRange(0,self.AUDIO_TRIM)
        self.end_slider.valueChanged.connect(self.call_update)
        self.layout.addWidget(self.end_slider)

        # Trim Lines
        self.is_trimming = False

        # Trim audio playback buttons
        self.trim_audio_begin_button = QPushButton('Play', self)
        self.trim_audio_begin_button.move(0, self.height() * 0.6)
        self.trim_audio_begin_button.clicked.connect(self.playback_on(self.begin_slider))
        
        self.trim_audio_end_button = QPushButton('Play', self)
        self.trim_audio_end_button.clicked.connect(self.playback_on(self.end_slider))
        self.trim_audio_end_button.move(0, self.height() * 0.7)

        # Trim audio text dialogue
        self.trim_audio_entry = QSpinBox(self)
        self.trim_audio_entry.move(0, self.height() * 0.8)
        self.layout.addWidget(self.trim_audio_entry)
        
        
        self.show()

    def call_update(self):
        self.update()
        
    def paintEvent(self, e):
#        print('ping')
        if self.is_trimming:
            qp = QPainter()
            qp.begin(self)

            # Draw Image
            rect = QRect(self.width() * 0.085, 0, WAV_IMAGE_WIDTH, WAV_IMAGE_HEIGHT)
            qp.drawPixmap(rect, QPixmap(self.current_page.wav_file + '.png'))

            def slider_x(slider):
                slider_start = slider.value()
                return (self.width() * 0.125) + ((slider_start/float(self.AUDIO_TRIM)) * 750
                        if slider_start != 0 else 0)

                        # Begin Line
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(slider_x(self.begin_slider), self.height() * 0.6, slider_x(self.begin_slider), 0)

            pen = QPen(Qt.red, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(slider_x(self.end_slider), self.height() * 0.6, slider_x(self.end_slider), 0)
            
            qp.end()
        else:
            qp = QPainter()
            qp.begin(self)
            qp.end()
        
    def run(self):

        # Get subject id
        # self.get_subect_info()
        self.next_page()

    def showLabel(self, label):
        # Edit phrase
        label.setWordWrap(True)
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
        self.title.setText("Recording off.")
        self.title.show()
        self.footer.setText('Press RETURN to continue')
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
        self.footer.setText('Press RETURN to complete trimming')
        
    def timer_tick(self, time_limit):
        def tick():
            interval = 100.0 / float(time_limit)
            self.timed_text.pacman.setValue(self.timed_text.pacman.value - interval)
            if self.timed_text.pacman.value == 0:
                self.recording_off()
        return tick

    def intro_complete(self):
        self.intro_screen.create_subject_id_and_folder()
        self.content = setup_study(self.intro_screen.subject_id)
        self.data_result.subject_id = self.subject_id
        self.next_page()

    def set_trimed_audio_time(self):
        start = self.begin_slider.value()/float(self.AUDIO_TRIM)
        end = self.end_slider.value() / float(self.AUDIO_TRIM )
        disruption = self.trim_audio_entry.value() * 0.01 # Convert from centiseconds to seconds
        with contextlib.closing(wave.open(self.current_page.wav_file + ".wav", 'r')) as r:
            frames = r.getnframes()
            rate = r.getframerate()
            duration = frames / float(rate)
            result_time = ((duration * end) - (duration * start)) - disruption
            print(str(result_time))
            self.base_recording_times[self.current_page.passage] = result_time
            self.data_result.time = result_time

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
            output.write(self.intro_screen.subject_info + str(self.data_result) + '\n')
    
    def next_page(self):
        self.spacebar_actions = []
        if(self.content):
            self.current_page = self.content.pop(0)
        else:
            # Restart experiment
            qApp.quit()

        # Just hide everything so each page doesn't have
        # to worry about what was already being dispalyed
        self.hide_all()
              
        if(type(self.current_page) is Intro):
            self.intro_screen.show()
            self.footer.setText('Press ENTER to continue')
            self.footer.show()
            
            self.enter_actions.append(self.intro_complete)
        
        # ------ Setup a Text  Window Page --------
        elif(type(self.current_page) is TextWindow):
            self.title.show()
            self.title.setText(self.current_page.header)
            self.title.adjustSize()
            self.phrase.show()
            self.phrase.setText(self.current_page.text)
            self.phrase.adjustSize()
            self.scroll_area.show()
            self.footer.setText(self.current_page.footer)
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
            self.title.setText('Press SPACE to begin recording')
            self.timed_text.setText(self.current_page.text)
            self.timed_text.pacman.value = 100
            self.showLabel(self.timed_text.scroll_text)
            self.timed_text.show()
            self.footer.setText('Press SPACE to begin recording')
            self.footer.show()
            self.data_result.target_file = self.intro_screen.subject_id + '/' + self.intro_screen.subject_id + '-timed.txt'
            self.data_result.is_base = False
            self.data_result.percentage = self.current_page.percentage
            
            base_time = self.base_recording_times[self.current_page.passage]
            record_time = base_time * self.current_page.percentage * 1000 # Converting to miliseconds
            self.timer.timeout.connect(self.timer_tick(record_time))
            print(str(record_time))
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
            self.begin_slider.show()
            self.trim_audio_begin_button.show()
            self.end_slider.show()
            self.trim_audio_end_button.show()
            self.trim_audio_entry.show()
            self.footer.setText('Press RETURN to continue')
            self.footer.show()
            self.is_trimming = True
            self.update()


            def trim_audio_action():
                self.set_trimed_audio_time()
                self.record_data_point()
                self.is_trimming = False
                self.update()
                
            self.enter_actions.append(trim_audio_action)


        elif(type(self.current_page) is Survey):
            self.questionnaire.show()
            self.footer.setText('Are you ready for the next one? Press ENTER to continue.')
            self.footer.show()

            def survey_action():
                self.record_survey_response()
                if not self.data_result.is_base:
                    self.record_data_point()
            
            self.enter_actions.append(survey_action)
                
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if not self.enter_actions and not self.spacebar_actions:
                self.next_page()
            elif not self.enter_actions:
                pass
            else:
                self.enter_actions.pop(0)()
                if not self.enter_actions:
                    self.next_page()
        elif event.key() == Qt.Key_Space:
            if len(self.spacebar_actions) > 0:
                self.spacebar_actions.pop(0)()
                

if __name__ == '__main__':
    while True:
        app = QApplication(sys.argv)
        ex = App()
        f = MyEventFilter(ex)
        app.installEventFilter(f)
        app.exec_()
        ex.close()

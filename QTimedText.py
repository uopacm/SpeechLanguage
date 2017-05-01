from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from QRoundProgressBar import *


class QTimedText(QWidget):
    def __init__(self, parent):
        super(QTimedText, self).__init__(parent)
        self.setGeometry(0, 0, 200, 200)
        self.layout = QGridLayout()
        
        self.pacman = QRoundProgressBar(self)
        self.pacman.setBarStyle(2) # Pie
        self.pacman.setFixedWidth(200)
        self.pacman.setFixedHeight(200)
        self.layout.addWidget(self.pacman)

        self.scroll_text = QLabel(self)
#        self.showLabel(self.scroll_text)
        self.scroll_text.adjustSize()
        self.scroll_text.setGeometry((self.width()-100)/2, (self.height()-100)/2 , 100, 100)
        self.layout.addWidget(self.scroll_text)
        

    def setText(self, text):
        self.scroll_text.setText(text)

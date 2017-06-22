import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QRadioButton, QButtonGroup
from PyQt5.QtCore import QSize

class Questionnaire(QWidget):
    def __init__(self, parent):
        super(Questionnaire, self).__init__(parent)
        self.layout = QGridLayout()
        self.setMinimumSize(QSize(parent.width() * 0.5, parent.height() * 0.5))

        # Add instructions at top
        self.instructions = QLabel("Rate the following statements for HOW MUCH you experienced: \n(1 being lowest, 5 being highest)", self)
        self.instructions.move(50, 10)
        self.instructions.adjustSize()
        self.layout.addWidget(self.instructions)

        # Questions go in here
        self.questions = ["1) Your need to read quickly","2) Your sense of a loss of control of speech", "3) Amount of anxiety during reading","4) Amount of time pressure experienced"]
        self.questions.reverse()

        # New button class for every question
        # Allows for Every question to have one answer
        Q1_response = QButtonGroup()
        Q2_response = QButtonGroup()
        Q3_response = QButtonGroup()
        Q4_response = QButtonGroup()
        self.button_group_questions = [Q1_response, Q2_response, Q3_response, Q4_response]

        # Counter for placement of questions/answers
        self.adjustCounter = 1

        for i in range(len(self.questions)):  # Display questions and add buttons to button groups
            self.addQuestion(self.button_group_questions[i-1])

        self.show()

    def addQuestion(self, button_group):
        buttonHeight = 60*self.adjustCounter+15  # Change y position of button sets

        self.newQuestion = QLabel(self.questions.pop(), self)  # Display every question
        self.newQuestion.move(50, 60*self.adjustCounter)
        self.newQuestion.adjustSize()
        self.layout.addWidget(self.newQuestion)

        count = 1  # Used for width between buttons
        options = ["1", "2", "3", "4", "5"]  # Display options of buttons
        buttons = [QRadioButton(option, self) for option in options]  # Make all options radio buttons

        # Display all radio buttons for this button group
        for button in buttons:
            button.move(50*count,buttonHeight)
            self.layout.addWidget(button)
            button_group.addButton(button)
            button.setCheckable(True)
            count += 1

        self.adjustCounter += 1  # Will adjust coordinates for next question
        
    def is_completed(self):
        for q in self.button_group_questions:
            if q.checkedId() == -1:
                return False
        return True

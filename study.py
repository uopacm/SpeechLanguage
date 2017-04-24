# Used to hold the content for and indicate a text only window
class TextWindow:
    def __init__(self, header, text, footer):
        self.header = header
        self.text = text
        self.footer = footer
        
# Used to hold the data for and indicate a base recording window
class BaseRecording:
    def __init__(self, output_file, text):
        self.text = text
        self.output_file = output_file

# Used to hold the data for and indicate a timed recording window
class TimedRecording:
    def __init__(self, text, output_file, base_time, percentage):
        self.text = text
        self.output_file = output_file
        self.base_time = base_time
        self.percentage = percentage

# Used to indicate a questionaire page
class Questionaire:
    def __init__(self):
        pass

def setup_study(subject):
    content = []
    content.append(TextWindow("Welcome and thank you for participating in our experiment!",
                   "First, we need a sample of your reading! The passage you will read is called \"The Rainbow Passage.\" When the passage is presented, press the spacebar when you start reading and press the spacebar again when you are finished reading.",
                   "Are you ready? Press the spacebar for the passage to appear."))
        
    content.append(BaseRecording(subject + "-rainbowtext.wav", "Insert the rainbow text here"))

    content.append(TextWindow("The First Phase",
                   "Nice reading! Now, it's time for the first phase of our experiment. You will presented with multiple reading tasks. Please read them out loud at your own natural pace. When you start reading, press the spacebar. When you finish reading, press the spacebar.\n\nAfter each reading task, a series of questions will be presented, asking you to rate you experience. Please answer each question on a scale of 1 to 5 (1=low, 5=high). Once you have finished answering the questions, please press the spacebar to start the next reading. Again, when you start reading, press the spacebar and when you finish reading, press the spacebar. If you have any questions about the task, please ask the examiner at this time.",                   "When you are ready to begin, press the spacebar to start."))
    return content


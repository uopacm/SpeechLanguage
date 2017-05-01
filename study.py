import json

# Used to hold the content for and indicate a text only window
class Intro:
    def __init__(self):
        pass

class TextWindow:
    def __init__(self, header, text, footer):
        self.header = header
        self.text = text
        self.footer = footer
        
# Used to hold the data for and indicate a base recording window
class BaseRecording:
    def __init__(self, output_file, text):
        self.text = text
        self.output_file = output_file + '.wav'

class TrimAudio:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        
# Used to hold the data for and indicate a timed recording window
class TimedRecording:
    def __init__(self,  output_file, base_time, percentage, text):
        self.text = text
        self.output_file = output_file
        self.base_time = base_time
        self.percentage = percentage

# Used to indicate a questionaire page
class Survey:
    def __init__(self, output):
        pass


def add_passages(subject, content, text):
    for passage in text:
        for (name, twister) in passage.items():
            file_name = subject + '/' + subject + name
            content.append(BaseRecording(file_name, twister))
            content.append(TrimAudio(file_name))
            content.append(Survey(file_name))
            
def setup_study(subject):

    with open('passages.json') as data_file:
        text = json.load(data_file)

        content = []

        content.append(TimedRecording('test.txt', 2.0, 1.0, 'This is a test\nA testy test\nThe most testy of all tests\n'))
    
        content.append(TextWindow("Welcome and thank you for participating in our experiment!",
                                  "First, we need a sample of your reading! The passage you will read is called \"The Rainbow Passage.\" When the passage is presented, press the spacebar when you start reading and press the spacebar again when you are finished reading.",
                                  "Are you ready? Press the spacebar for the passage to appear."))
    
        content.append(BaseRecording(subject + '/' + subject + "-rainbow-text", text['rainbow'][0]['rainbow']))

        content.append(TrimAudio(subject +'/'+subject + '-rainbow-text'))
    
        content.append(TextWindow("The First Phase",
                                  "Nice reading! Now, it's time for the first phase of our experiment. You will presented with multiple reading tasks. Please read them out loud at your own natural pace. When you start reading, press the spacebar. When you finish reading, press the spacebar.\n\nAfter each reading task, a series of questions will be presented, asking you to rate you experience. Please answer each question on a scale of 1 to 5 (1=low, 5=high). Once you have finished answering the questions, please press the spacebar to start the next reading. Again, when you start reading, press the spacebar and when you finish reading, press the spacebar. If you have any questions about the task, please ask the examiner at this time.",                   "When you are ready to begin, press the spacebar to start."))

        add_passages(subject, content, text['twisters'])
        add_passages(subject, content, text['anomalous'])
            
    return content


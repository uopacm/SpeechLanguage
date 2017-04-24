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
        
    content.append(BaseRecording(subject + "-rainbowtext.wav", "When the sunlight strikes raindrops in the air, they act like a prism and form a rainbow. The rainbow is a division of white light into many beautiful colors. These take the shape of a long round arch, with its path high above, and its two ends apparently beyond the horizon. There is, according to legend, a boiling pot of gold at one end. People look, but no one ever finds it. When a man looks for something beyond his reach, his friends say he is looking for the pot of gold at the end of the rainbow.\n\nThroughout the centruies men have explained the rainbow in various ways. Some have accepted it as a miracle without physical explanation. To the Hebrews it was a token that there would be no more universal floods. The Greeks used to imagine that it was a sign from the gods to foretell war or heavy rain. The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky. Other men have tried to explain the phenomenon physically. Aristotle thought that the rainbow was caused by the reflection of the sun's rays by the rain. Since then physicists have found that it is not reflection, but refraction by the raindrops which causes the rainbow.\n\nMany complicated ideas about the rainbow have been formed. The difference in the rainbow depends considerably upon the size the water drops, and the width of the colored band increases as the size of the drops increases. The actual primary rainbow observed is said to be the effect of superposition of a number of bows. If the result is to give a bow with an abnormally wide yellow band, since red and green lights when mixed form yellow. This is a very common type of bow, one showing mainly red and yellow, with little or no green or blue."))

    content.append(TextWindow("The First Phase",
                   "Nice reading! Now, it's time for the first phase of our experiment. You will presented with multiple reading tasks. Please read them out loud at your own natural pace. When you start reading, press the spacebar. When you finish reading, press the spacebar.\n\nAfter each reading task, a series of questions will be presented, asking you to rate you experience. Please answer each question on a scale of 1 to 5 (1=low, 5=high). Once you have finished answering the questions, please press the spacebar to start the next reading. Again, when you start reading, press the spacebar and when you finish reading, press the spacebar. If you have any questions about the task, please ask the examiner at this time.",                   "When you are ready to begin, press the spacebar to start."))

    return content


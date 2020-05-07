from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox 
from kivy.uix.popup import Popup
import time

current_question = 0
total_answered = 0
total_correct = 0

questions = [
    {
        'question': 'What is a correct syntax to output "Hello World" in Python?',
        'answers': ['p("Hello World")', 'echo("Hello World")', 'print("Hello World")', 'echo "Hello World"'], 
        'correct': 'print("Hello World")'
    },
    {
        'question':'How do you insert COMMENTS in Python code?', 
        'answers': ['#This is a comment', '//This is a comment', '/*This is a comment*/'], 
        'correct': '#This is a comment'
    },
    {
        'question': 'How do you create a variable with the numeric value 5?', 
        'answers': ['x=int(5)', 'x=5', 'Both answers are correct'], 
        'correct': 'Both answers are correct'
    },
    {
        'question': 'What is the correct file extension for Python files?', 
        'answers': ['.pyt', '.pyth', '.pt', '.py'], 
        'correct': '.py'
    },
    {
        'question': 'What is the correct way to create a function in Python?', 
        'answers': ['def myFunction():', 'create myFunction():', 'function myFunction():'], 
        'correct': 'def myFunction():'
    },
]


class QuizScreen(App):
    def build(self):
        self.main_layout = BoxLayout(orientation="vertical")        
        title_w = Label(text='WELCOME To the Python Quiz App'.upper(),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      
                      )
        title_w.bold = True
        #title_w.font_size = '40sp'
        self.main_layout.add_widget(title_w) 

        footer = BoxLayout(pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(.5, 0.2))
        begin_button = Button(
                text="Begin",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(.4, 0.5)
                
            )
        begin_button.bind(on_press=self.start_quiz)  
        footer.add_widget(begin_button)     
        self.main_layout.add_widget(footer)
        return self.main_layout
    

    def start_quiz(self, instance):
        global current_question
        global total_correct
        current_question = 0
        total_correct = 0

        self.main_layout.clear_widgets()

        title = Label(text='PYTHON QUIZ',
                      pos_hint={'center_x': .5, 'center_y': .5},
                      )
        title.text_size = title.size
        title.bold = True
        self.main_layout.add_widget(title)
        
        qNbr = "Question " + str(current_question + 1)
        self.qtitle = Label(text = str(qNbr).upper(),
                      pos_hint={'center_x': .5, 'center_y': .5},)
        self.qtitle.bold = True
        self.question = Label(text=questions[current_question]["question"],
                    halign="left",
                      pos_hint={'center_x': 0.5, 'center_y': .5}
                      )
        self.main_layout.add_widget(self.qtitle)
        self.main_layout.add_widget(self.question)

        self.answers = BoxLayout(orientation="vertical")
        self.choices = []
        for answer in questions[current_question]["answers"]:
            answer_row = BoxLayout()
            answer_row.size_hint = (0.5, 1)
            answer_row.pos_hint = {'center_x': .5, 'center_y': .5}
            
            option_lbl = Label(text=answer, pos_hint={'center_x': .5, 'center_y': .5})
            option_checkbox = CheckBox()
            option_checkbox.group = "answer"

            answer_row.add_widget(option_checkbox)
            answer_row.add_widget(option_lbl)
            self.answers.add_widget(answer_row)
            self.choices.append([option_checkbox, option_lbl])

        self.main_layout.add_widget(self.answers)

        navigation = BoxLayout(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(.7, 0.6))
        previous_button = Button(
                text="Previous",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(.3, 0.4)
            )
        previous_button.bind(on_press=self.on_previous_button_press)
        navigation.add_widget(previous_button)
        next_button = Button(
                text="Next",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(.3, 0.4)
                
            )
        next_button.bind(on_press=self.on_next_button_press)
        navigation.add_widget(next_button)
        self.main_layout.add_widget(navigation)


    def load_answers(self):
        global current_question
        self.answers.clear_widgets()
        self.choices = []
        for answer in questions[current_question]["answers"]:
            answer_row = BoxLayout()
            answer_row.size_hint = (0.5, 1)
            answer_row.pos_hint = {'center_x': .5, 'center_y': .5}
            
            option_lbl = Label(text=answer, pos_hint={'center_x': .5, 'center_y': .5})
            option_checkbox = CheckBox()
            option_checkbox.group = "answer"

            answer_row.add_widget(option_checkbox)
            answer_row.add_widget(option_lbl)
            self.answers.add_widget(answer_row)
            self.choices.append([option_checkbox, option_lbl])


    def on_previous_button_press(self, instance):
        global current_question
        print("previous pressed from Q" + str(current_question + 1))
        if current_question == 0:
            return
        current_question -= 1
        self.question.text = questions[current_question]["question"]
        self.qtitle.text = ("Question " + str(current_question + 1)).upper()
        self.load_answers()


    def get_selected_radio_value(self):
        for row in self.choices:
            if row[0].active == True:
                return row[1].text
        return ""


    def on_next_button_press(self, instance):
        global current_question
        global total_correct
        print("next pressed from Q" + str(current_question + 1))
        if current_question == len(questions)-1:
            print("quiz completed")
            popup = Popup(title='Congratulations',
                            content=Label(text='Yay! You completed the Quiz!'
                            + '\nyou scored ' + str(total_correct) + "/" + str(len(questions))),
                            size_hint=(.5, 0.3))
            popup.open()
            self.end_choice()
            return        
        
        # check correct answer
        selected = self.get_selected_radio_value()
        if selected == questions[current_question]["correct"]:
            total_correct += 1
            popup = Popup(title='Feedback',
                            content=Label(text='Good Job! Correct!'),
                            size_hint=(.5, 0.3))
            popup.open()
        else:
            popup = Popup(title='Feedback',
                            content=Label(text='Too Bad. You missed that one\n The correct answer is "'+ questions[current_question]["correct"] +'"'),
                            size_hint=(.5, 0.3))
            popup.open()

        current_question += 1
        self.question.text = questions[current_question]["question"]
        self.qtitle.text = ("Question " + str(current_question + 1)).upper()
        self.load_answers()

    
    def end_choice(self):
        global current_question
        global total_correct

        self.main_layout.clear_widgets()      
        title_g = Label(text='Thanks for learning with us'.upper(),
                      pos_hint={'center_x': .5, 'center_y': .5},
                       size_hint=(.5, 0.3)
                      )
        self.main_layout.add_widget(title_g) 

        footer1 = BoxLayout(pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(.4, 0.2))
        retry_button = Button(
                text="Retry",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(.4, 0.4)
                
            )
        retry_button.bind(on_press=self.start_quiz)  
        footer1.add_widget(retry_button)     
        self.main_layout.add_widget(footer1)

        footer2 = BoxLayout(pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(.4, 0.2))
        quit_button = Button(
                text="Quit",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(.4, 0.4)
                
            )
        quit_button.bind(on_press=self.stop)  
        footer2.add_widget(quit_button)     
        self.main_layout.add_widget(footer2)


# # Create the screen manager
# sm = ScreenManager()
# welcome = WelcomeScreen(name='welcome')
# welcome.build()
# sm.add_widget(welcome)
# quiz = QuizScreen(name='quiz')
# quiz.build()
# sm.add_widget(quiz)
# sm.current = 'welcome'

# class MyQuizApp(App):
#     def build(self):
#         return sm

if __name__ == '__main__':
    QuizScreen().run()


# if __name__ == '__main__':
#     app = QuizScreen()
#     app.run()
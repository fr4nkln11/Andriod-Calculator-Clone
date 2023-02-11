import re
import math
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex as hexColor 

Window.clearcolor = hexColor('#dddddd') #Changes the window color

# Register custom fonts
LabelBase.register(name = 'Roboto',
        fn_regular = 'Roboto-Thin.ttf',
        fn_bold = 'Roboto-Regular.ttf')
        
# trigonometric functions that return degrees instead of radians
def sin(num):
    return math.sin(math.radians(num))
        
def cos(num):
    return math.cos(math.radians(num))
        
def tan(num):
    return math.tan(math.radians(num))
        
# The main app
class CalculatorApp(App):
    """ This is a simple calculator app which is designed to work
    like a clone of the original android calculator"""
    
    # Colors used 
    colors = {
        'white': hexColor('#ffffff'),
        'red': hexColor('#ff0000'),
        'green': hexColor('#00ff00'),
        'grey': hexColor('#dddddd'),
        'black': hexColor('#000000')
    }
    
    # checks if the equal button is pressed
    equal_pressed = False
    
    def make_evaluable(self, exp):
        """ converts the screen label string into an evaluable
        expression"""
        # using normal replace function to replace unrecognized symbols
        exp = exp.replace('÷', '/')
        exp = exp.replace('×', '*')
        exp = exp.replace('^', '**')
        exp = exp.replace('π', 'math.pi')  
        exp = exp.replace('e', 'math.e')
        
        # using regex for complex replacements
        exp = re.sub(r'√(\d+)', r'math.sqrt(\1)', exp)
        exp = re.sub(r'(\d+)!', r'math.factorial(\1)', exp)
        exp = re.sub(r'(\d+)\((\d+)\)', r'\1*(\2)', exp)
        exp = re.sub(r'(\d+)\)\(', r'\1)*(', exp)
        exp = re.sub(r'(\d+)\((\d+)', r'\1*\2', exp)
        exp = re.sub(r'(\d+)math.pi', r'\1*math.pi', exp)
        
        return exp
    
    def keypad_press(self, text):
        """ display text on the screen label once a button is pressed"""
        self.root.ids.screen.text = self.root.ids.screen.text + str(text)
        self.auto_solve()
        
    def delete_clear(self):
        """ deletes text and clears the entire screen label"""
        if self.equal_pressed:
            self.root.ids.screen.text = ""
            self.root.ids.res_screen.text = ""
            self.equal_pressed = False
            self.root.ids.del_clr_btn.text = "DEL"
            self.root.ids.res_screen.color = (.3,.3,.3,.6)
        else:
            exp = list(self.root.ids.screen.text)
            if ''.join(exp[len(exp) - 2:]) in {'n(', 's('}:
                del exp[len(exp) - 4:]
            elif len(exp) > 0:
                exp.pop()
            self.root.ids.screen.text = ''.join(exp)
            self.auto_solve()
        
    def solve(self):
        """ solves the expression on the screen label"""
        if self.root.ids.screen.text == '':
            return
        try:
            self.equal_pressed = True
            exp = self.root.ids.screen.text
            exp = self.make_evaluable(exp)
            solution = eval(exp)
            self.root.ids.screen.text = str(round(solution, 5))
            self.root.ids.res_screen.text = ''
        except SyntaxError:
            self.root.ids.res_screen.text = "Syntax Error"
            self.root.ids.res_screen.color = self.colors['red']
        except ZeroDivisionError:
            self.root.ids.res_screen.text = "Infinty"
            self.root.ids.res_screen.color = self.colors['red']

        self.root.ids.del_clr_btn.text = "CLR"

    def check_evaluable(self, exp):
        """ checks if the expression text on the screen label can be evaluated without an error"""
        try:
            eval(exp)
            return True
        except (SyntaxError, ZeroDivisionError):
            return False
    
    def auto_solve(self):
        """ automatically solves the expression only if it is evaluable"""
        exp = self.root.ids.screen.text
        exp = self.make_evaluable(exp)
        if self.check_evaluable(exp):
            self.root.ids.res_screen.color = (.3, .3, .3, .6)
            self.root.ids.res_screen.text = str(round(eval(exp), 5))
        else:
            self.root.ids.res_screen.text = ''
    
if __name__ == '__main__':
    CalculatorApp().run()

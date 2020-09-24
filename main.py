import re
import math
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex as hexColor
from string import digits

Window.clearcolor = hexColor('#dddddd')
LabelBase.register(name = 'Roboto',
        fn_regular = 'fonts/Roboto-Thin.ttf',
        fn_bold = 'fonts/Roboto-Regular.ttf')
        
def sin(num):
        return math.sin(math.radians(num))
        
class CalculatorApp(App):
    colors = {
        'white': hexColor('#ffffff'),
        'red': hexColor('#ff0000'),
        'green': hexColor('#00ff00'),
        'grey': hexColor('#dddddd'),
        'black': hexColor('#000000')
    }
    
    equal_pressed = False
    
    def make_evaluable(self, exp):
        exp = exp.replace('÷', '/')
        exp = exp.replace('×', '*')
        exp = exp.replace('^', '**')
        exp = exp.replace('π', 'math.pi')  
        exp = exp.replace('e', 'math.e')
             
        exp = re.sub(r'√(\d+)', r'math.sqrt(\1)', exp)
        exp = re.sub(r'(\d+)!', r'math.factorial(\1)', exp)
        exp = re.sub(r'(\d+)\((\d+)\)', r'\1*(\2)', exp)
        exp = re.sub(r'(\d+)\)\(', r'\1)*(', exp)
        exp = re.sub(r'(\d+)\((\d+)', r'\1*\2', exp)
        exp = re.sub(r'(\d+)math.pi', r'\1*math.pi', exp)
        
        
        print(exp)  
        return exp
    
    def keypad_num_press(self, num):
        self.root.ids.screen.text = self.root.ids.screen.text + str(num)
        self.auto_solve()
        
    def delete_clear(self):
        if self.equal_pressed:
            self.root.ids.screen.text = ""
            self.root.ids.res_screen.text = ""
            self.equal_pressed = False
            self.root.ids.del_clr_btn.text = "DEL"
            self.root.ids.res_screen.color = (.3,.3,.3,.6)
        else:
            exp = list(self.root.ids.screen.text)
            if ''.join(exp[len(exp) - 2:]) in ('n(', 's('):
                del exp[len(exp) - 4:]
            elif len(exp) > 0:
                exp.pop()
            self.root.ids.screen.text = ''.join(exp)
            self.auto_solve()
        
    def solve(self):
        if self.root.ids.screen.text != '':
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
                self.root.ids.res_screen.text = "Complex Infinty"
                self.root.ids.res_screen.color = self.colors['red']
                
            self.root.ids.del_clr_btn.text = "CLR"

    def check_evaluable(self, exp):
        try:
            eval(exp)
            return True
        except (SyntaxError, ZeroDivisionError):
            return False
    
    def auto_solve(self):
        exp = self.root.ids.screen.text
        exp = self.make_evaluable(exp)
        if self.check_evaluable(exp):
            self.root.ids.res_screen.color = (.3, .3, .3, .6)
            self.root.ids.res_screen.text = str(round(eval(exp), 6))
        else:
            self.root.ids.res_screen.text = ''    
    
if __name__ == '__main__':
    CalculatorApp().run()

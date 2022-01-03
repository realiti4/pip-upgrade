import os
import sys

class ColoredPrint():
    def __init__(self):
        self.enabled = True
        self.color_dict = {
            'green': '\033[32m',
            'yellow': 'notimplemented',
            'default': '\033[m'
        }
        if self.terminal_check:
            self.enabled = False

    def terminal_check(self):
        """Don't print colored if it is cmd"""
        return (os.getenv('PROMPT', '') == '$P$G')

    def __call__(self, *input, color='green', disabled=False):
        if disabled or not self.enabled:
            print(*input)
        else:
            if isinstance(input, tuple):
                print(f"{self.color_dict[color]}{input[0]}{self.color_dict['default']}", *input[1:])
            else:
                print(f"{self.color_dict[color]}{input}{self.color_dict['default']}")     

if __name__ == '__main__':
    cprint = ColoredPrint()
    cprint('heey', 'ha')
    print('de')
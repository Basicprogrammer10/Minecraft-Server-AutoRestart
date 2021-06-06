from datetime import datetime

COLOR_CODES = {'black': '30', 'red': '31', 'yellow': '33', 'green': '32', 'blue': '34',
              'cyan': '36', 'magenta': '35', 'white': '37', 'gray': '90', 'reset': '0'}

def getLastOfArray(array):
    """Return the value of the last index of an array"""
    return array[len(array)-1]

def colored(text, color):
    """Add the ansi color codes to text to give it color when printed"""
    return '\033[' + COLOR_CODES[str(color).lower()] + 'm' + str(text) + "\033[0m"

def debugPrint(Category, Text, Color):
    """Format a print with the current time, a category and colored text"""
    print(f"{colored('['+datetime.now().strftime('%H:%M:%S')+']', 'yellow')} {colored('['+Category+']', 'magenta')} {colored(Text, Color)}")
    
def makeRealNewLine(text):
    """Convert \n's to newlines"""
    return text.replace('\\n', '\n')

__all__ = ['getLastOfArray', 'colored', 'debugPrint']
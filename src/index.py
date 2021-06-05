from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
import os
import re

########### CONFIG ###########
toRun = ["java", "-Xmx1G", "-jar", "server.jar", "--nogui"]

############ VARS ############
DEBUG = True
COLOR = True

ColorCodes = {'black': '30', 'red': '31', 'yellow': '33', 'green': '32', 'blue': '34',
              'cyan': '36', 'magenta': '35', 'white': '37', 'gray': '90', 'reset': '0'}

######### FUNCTIONS #########
def colored(text, color):
    if not COLOR: return text
    return '\033[' + ColorCodes[str(color).lower()] + 'm' + str(text) + "\033[0m"


def DebugPrint(Category, Text, Color):
    if not DEBUG: return
    print(f"{colored('['+datetime.now().strftime('%H:%M:%S')+']', 'yellow')} {colored('['+Category+']', 'magenta')} {colored(Text, Color)}")


def getLastOfArray(array):
    return array[len(array)-1]


####### MAIN FUNCTION #######
def main():
    process = Popen(toRun, stdout = PIPE, stderr = STDOUT)
    while True:
        line = process.stdout.readline()
        text = line.decode("utf-8").replace('\n', '')
        text = getLastOfArray(text.split('] '))
        DebugPrint('Server', text, 'magenta')
        if not line: break
    exit_code = process.wait()
    DebugPrint('Main', 'Server Closed' if exit_code == 0 else 'Server Crashed', 'red')
    if exit_code != 0:
        DebugPrint('Main', 'Trying to Restart Server', 'blue')
        main()

if __name__ == "__main__":
    os.chdir('server')
    DebugPrint('Main', 'Starting...', 'green')
    try: main()
    except: DebugPrint('Main', 'Exiting...', 'red')
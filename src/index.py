from subprocess import Popen, PIPE, STDOUT
import os

import common

########### CONFIG ###########
toRun = ["java", "-Xmx1G", "-jar", "server.jar", "--nogui"]


######### FUNCTIONS #########


####### MAIN FUNCTION #######
def main():
    process = Popen(toRun, stdout = PIPE, stderr = STDOUT) # Open a pipe to the minecraft server

    # Read and print the servers Std Out
    while True:
        line = process.stdout.readline()
        text = line.decode("utf-8").replace('\n', '')
        text = common.getLastOfArray(text.split('] '))
        common.debugPrint('Server', text, 'magenta')
        if not line: break

    # Get ExitCode when server stops
    exit_code = process.wait()
    common.debugPrint('Main', 'Server Closed' if exit_code == 0 else 'Server Crashed', 'red')

    # If exit code is Non 0 then start the server again
    if exit_code != 0:
        common.debugPrint('Main', 'Trying to Restart Server', 'blue')
        main()

if __name__ == "__main__":
    os.chdir('server')
    common.debugPrint('Main', 'Starting...', 'green')
    try: main()
    except: common.debugPrint('Main', 'Exiting...', 'red')
from subprocess import Popen, PIPE, STDOUT, run
import os

import common
import discord

########### CONFIG ###########
toRun = ["java", "-Xmx1G", "-jar", "server.jar", "--nogui"]
webhookUri = ''


######### FUNCTIONS #########
def runServer(webhook):
    process = Popen(toRun, stdout = PIPE, stderr = STDOUT) # Open a pipe to the minecraft server

    # Read and print the servers Std Out
    while True:
        line = process.stdout.readline()
        text = line.decode("utf-8").replace('\n', '')
        text = common.getLastOfArray(text.split('] '))
        if not line: break
        if text == '': continue
        common.debugPrint('Server', text, 'magenta')      
        print(webhook.sendText(text))

    # Get ExitCode when server stops
    exit_code = process.wait()
    common.debugPrint('Main', 'Server Closed' if exit_code == 0 else 'Server Crashed', 'red')

    # If exit code is Non 0 then start the server again
    if exit_code != 0:
        common.debugPrint('Main', 'Trying to Restart Server', 'blue')
        runServer()

####### MAIN FUNCTION #######
def main():
    # Create a new webhook client
    webhook = discord.webhook(webhookUri)

    os.chdir('server')
    common.debugPrint('Main', 'Starting...', 'green')
    runServer(webhook)

if __name__ == "__main__":
    try: main()
    except: common.debugPrint('Main', 'Exiting...', 'red')
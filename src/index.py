# Import Modules
from subprocess import Popen, PIPE, STDOUT, run
import os
import re

# Import Custom Modules
import common
import discord

########### CONFIG ###########
toRun = ["java", "-Xmx1G", "-jar", "server.jar", "--nogui"]

# Discord Webhook Uri
webhookUri = ''

# If sending webhooks should be enabled
webhooks   = webhookUri != ''


######### FUNCTIONS #########
def parseServerOut(webhook, text):
    # On server Start
    if re.match(r'\[.*\]: Done', text):
        webhook.send(':star2: Server Started!')

    # On user chat message
    if re.match(r'\[.*\]: <.*> .*', text):
        sender = text.split('<')[1].split('>')[0]
        message = text.split('> ')[1]
        message = common.makeRealNewLine(message)
        webhook.send(f'{sender} » {message}')

    # On user Join
    if 'joined the game' in text:
        user = text.split(': ')[1].split(' joined the game')[0]
        webhook.send(f':white_check_mark: **{user}** joined the game')

    # On user leave
    if 'left the game' in text:
        user = text.split(': ')[1].split(' left the game')[0]
        webhook.send(f':x: **{user}** left the game')

def runServer(webhook):
    # Open a pipe to the minecraft server
    process = Popen(toRun, stdout = PIPE, stderr = STDOUT)

    # Read and print the servers Std Out
    while True:
        line = process.stdout.readline()
        text = line.decode("utf-8").replace('\n', '')
        text = common.getLastOfArray(text.split('] '))
        if not line: break
        if text == '': continue
        common.debugPrint('Server', text, 'magenta')     
        parseServerOut(webhook, text) 

    # Get ExitCode when server stops
    exit_code = process.wait()
    common.debugPrint('Main', 'Server Closed' if exit_code == 0 else 'Server Crashed', 'red')

    # If exit code is Non 0 then start the server again
    if exit_code != 0:
        common.debugPrint('Main', 'Trying to Restart Server', 'blue')
        webhook.send(':fire: Server Crash :/ - Attempting Restart')
        runServer(webhook)
    if exit_code == 0:
        webhook.send(':stop_button: Server Stoped...')

####### MAIN FUNCTION #######
def main():
    # Create a new webhook client thing...
    webhook = discord.webhook(webhookUri, webhooks)

    os.chdir('server')
    common.debugPrint('Main', 'Starting...', 'green')
    runServer(webhook)

if __name__ == "__main__":
    try: main()
    except: common.debugPrint('Main', 'Exiting...', 'red')
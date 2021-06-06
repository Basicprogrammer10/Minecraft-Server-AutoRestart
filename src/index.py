# Import Modules
from subprocess import Popen, PIPE, STDOUT, run
import os
import re

# Import Custom Modules
import common
import discord
import config

########### CONFIG ###########
configFile = 'config/config.confnose'
version = 'Alpha 1.3'


######### FUNCTIONS #########
def parseServerOut(webhook, text):
    # On server Start
    if re.match(r'\[.*\]: Done \(.*\)!', text):
        webhook.send(':star2: Server Started!')
        return

    # On user chat message
    if re.match(r'\[.*\]: <.*> .*', text):
        sender = text.split('<')[1].split('>')[0]
        message = text.split('> ')[1]
        message = common.makeRealNewLine(message)
        webhook.send(f':speech_left: **{sender}** » {message}')
        return

    # On user Advancement / Challenge complete
    if re.match(r'.* has (made|completed) the (advancement|challenge) \[.*\]', text):
        user = text.split(': ')[1].split(' ')[0]
        adv = common.getLastOfArray(text.split('[')).split(']')[0]
        thing = 'advancement' if 'advancement' in text else 'challenge'
        webhook.send(f':dvd: **{user}** has completed the {thing} **{adv}**')
        return

    # On user Join
    if 'joined the game' in text:
        user = text.split(': ')[1].split(' joined the game')[0]
        webhook.send(f':white_check_mark: **{user}** joined the game')
        return

    # On user leave
    if 'left the game' in text:
        user = text.split(': ')[1].split(' left the game')[0]
        webhook.send(f':x: **{user}** left the game')
        return

def runServer(cfg, webhook):
    # Open a pipe to the minecraft server
    process = Popen(cfg.get('toRun'), stdout = PIPE, stderr = STDOUT)

    # Read and print the servers Std Out
    while True:
        try:
            line = process.stdout.readline()
            text = line.decode("utf-8").replace('\n', '')
            text = common.getLastOfArray(text.split('] '))
            if not line: break
            if text == '': continue
            common.debugPrint('Server', text, 'magenta')     
            parseServerOut(webhook, text)
        except Exception as e:
            common.debugPrint('Main', 'Uhhh... Houston, we have a problem.', 'red')
            print(common.colored(e, 'red'))

    # Get ExitCode when server stops
    exit_code = process.wait()
    common.debugPrint('Main', 'Server Closed' if exit_code == 0 else 'Server Crashed', 'red')

    # If exit code is Non 0 then start the server again
    if exit_code != 0:
        common.debugPrint('Main', 'Trying to Restart Server', 'blue')
        webhook.send(':fire: Server Crash :/ - Attempting Restart')
        runServer(cfg, webhook)
    if exit_code == 0:
        webhook.send(':stop_button: Server Stoped...')

####### MAIN FUNCTION #######
def main():
    # Nice Welcome Message
    common.debugPrint('Main', f'Welcome to Minecraft Server AutoRestart! {version}', 'cyan')

    # Load Config
    cfg = config.config(configFile)
    cfg.read()

    # Create a new webhook client thing...
    webhook = discord.webhook(cfg.get('webhookUri'), cfg.get('webhooks'))

    # Set webhook name to be current webhook name + version of this program
    webhook.name(f'{webhook.name()} - {version}')

    os.chdir(cfg.get('serverFolder', 'server'))
    common.debugPrint('Main', 'Starting...', 'green')
    runServer(cfg, webhook)

if __name__ == "__main__":
    main()
    exit()
    try: main()
    except: common.debugPrint('Main', 'Exiting...', 'red')
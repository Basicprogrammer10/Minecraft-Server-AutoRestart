# Import Modules
from subprocess import Popen, PIPE, STDOUT, run
import os
import re

# Import Custom Modules
import common
import discord
import config
import events

########### CONFIG ###########
configFile = 'config/config.confnose'
version = 'Alpha 1.32'


######### FUNCTIONS #########
def parseServerOut(webhook, text):
    thisEvent = events.event(webhook, text)

    # On server Start
    if re.match(r'\[.*\]: Done \(.*\)!', text): thisEvent.serverStart()

    # On user chat message
    if re.match(r'\[.*\]: <.*> .*', text): thisEvent.chatMessage()

    # On user Advancement / Challenge complete
    if re.match(r'.* has (made|completed) the (advancement|challenge) \[.*\]', text): thisEvent.advancement()

    # On user Join
    if 'joined the game' in text: thisEvent.joinGame()

    # On user leave
    if 'left the game' in text: thisEvent.leaveGame()

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
        events.event(webhook).serverCrash()
        runServer(cfg, webhook)
    if exit_code == 0:
        events.event(webhook).serverStop()

####### MAIN FUNCTION #######
def main():
    # Nice Welcome Message
    common.debugPrint('Main', f'Welcome to Minecraft Server AutoRestart! {version}', 'cyan')

    # Plugin Loading
    for i in common.getAllPlugins('src/plugins'):
        print(common.loadPlugin(f'plugins.{i}'))
    #from plugins.examplePlugin import plugin
    #print(plugin().name)
    exit()

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
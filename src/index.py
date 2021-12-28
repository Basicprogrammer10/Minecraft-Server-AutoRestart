# Import Modules
from subprocess import Popen, PIPE, STDOUT, run
import traceback
import os
import re

# Import Custom Modules
import common
import discord
import config
import events

########### CONFIG ###########
configFile = 'config/config.confnose'
version = 'Alpha 2.4'


######### FUNCTIONS #########
def parseServerOut(webhook, text, pluginEvents):
    # Check for plugin Events
    run = []
    for i in pluginEvents:
        if re.match(pluginEvents[i], text):  run.append(i(webhook, text))

    return run

def runServer(cfg, webhook, pluginEvents):
    # Open a pipe to the minecraft server
    process = Popen(
            cfg.get('toRun'),
            stdout = PIPE,
            stdin = PIPE if cfg.get('autoStdIn') else None,
            stderr = STDOUT,
            shell = cfg.get('openShell', False)
        )

    # Read and print the servers Std Out
    while True:
        try:
            line = process.stdout.readline()
            text = line.decode("utf-8").replace('\n', '')
            text = "] ".join(text.split('] ')[-1:])
            if not line: break
            if text == '': continue
            common.debugPrint('Server', f'{text}', 'magenta')
            toWrite = parseServerOut(webhook, text, pluginEvents)
            if toWrite != []:
                for i in toWrite:
                    if i == None: continue
                    process.communicate(input = i.encode())
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
        runServer(cfg, webhook, pluginEvents)
    if exit_code == 0:
        events.event(webhook).serverStop()

####### MAIN FUNCTION #######
def main():
    # Nice Welcome Message
    common.debugPrint('Main', f'Welcome to Minecraft Server AutoRestart! {version}', 'cyan')

    # Plugin Loading
    pluginEvents = {}
    plugins = common.getAllPlugins('src/plugins')
    plugins.append('events')
    for i in plugins:
        plugin = common.loadPlugin(f'{"plugins." if "events" not in i else ""}{i}')
        if plugin == None: continue
        common.debugPrint('PluginLoader', f'Loading {plugin["name"]} - {plugin["version"]}', 'blue')
        for j in plugin['events']:
            pluginEvents[j] = plugin['events'][j]

    # Load Config
    cfg = config.config(configFile)
    cfg.read()

    # Create a new webhook client thing...
    webhook = discord.webhook(cfg.get('webhookUri'), cfg.get('webhooks'))

    # Set webhook name to be current webhook name - version of this program
    webhook.name(f'{webhook.name()} - {version}')

    # Change Working dir to Server dir
    os.chdir(cfg.get('serverFolder', 'server'))

    common.debugPrint('Main', 'Starting...', 'green')
    runServer(cfg, webhook, pluginEvents)

if __name__ == "__main__":
    try: main()
    except:
        common.debugPrint('Main', 'Exiting...', 'red')
        print(traceback.print_exc())

import common

# Basic Events
class event():
    def __init__(self, webhook):
        self.webhook = webhook

    def serverStop(self):
        self.webhook.send(':stop_button: Server Stopped...')

    def serverCrash(self):
        self.webhook.send(':fire: Server Crash :/ - Attempting Restart')

# Events with stdOut Regexes
class plugin():
    def __init__(self):
        self.name = 'Built In Events'
        self.version = '1.0'
        self.doRun = True

    def serverStart(self, webhook, rawData) -> '\[.*\]: Done \(.*\)!':
        webhook.send(':star2: Server Started!')

    def chatMessage(self, webhook, rawData) -> '\[.*\]: <.*> .*':
        sender = rawData.split('<')[1].split('>')[0]
        message = rawData.split('> ')[1]
        message = common.makeRealNewLine(message)
        webhook.send(f':speech_left: **{sender}** » {message}')

    def advancement(self, webhook, rawData) -> '.* has (made|completed) the (advancement|challenge) \[.*\]':
        user = rawData.split(': ')[1].split(' ')[0]
        adv = rawData.split('[')[-1].split(']')[0]
        thing = 'advancement' if 'advancement' in rawData else 'challenge'
        webhook.send(f':dvd: **{user}** has completed the {thing} **{adv}**')

    def joinGame(self, webhook, rawData) -> '\[.*\]: .* joined the game':
        user = rawData.split(': ')[1].split(' joined the game')[0]
        webhook.send(f':white_check_mark: **{user}** joined the game')

    def leaveGame(self, webhook, rawData) -> '\[.*\]: .* left the game':
        user = rawData.split(': ')[1].split(' left the game')[0]
        webhook.send(f':x: **{user}** left the game')

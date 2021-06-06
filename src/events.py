import common

class event():
    def __init__(self, webhook, rawData = None):
        self.webhook = webhook
        self.rawData = rawData

    def serverStart(self):
        self.webhook.send(':star2: Server Started!')
    
    def serverStop(self):
        self.webhook.send(':stop_button: Server Stoped...')

    def serverCrash(self):
        self.webhook.send(':fire: Server Crash :/ - Attempting Restart')

    def chatMessage(self):
        sender = self.rawData.split('<')[1].split('>')[0]
        message = self.rawData.split('> ')[1]
        message = common.makeRealNewLine(message)
        self.webhook.send(f':speech_left: **{sender}** » {message}')

    def advancement(self):
        user = self.rawData.split(': ')[1].split(' ')[0]
        adv = common.getLastOfArray(self.rawData.split('[')).split(']')[0]
        thing = 'advancement' if 'advancement' in self.rawData else 'challenge'
        self.webhook.send(f':dvd: **{user}** has completed the {thing} **{adv}**')

    def joinGame(self):
        user = self.rawData.split(': ')[1].split(' joined the game')[0]
        self.webhook.send(f':white_check_mark: **{user}** joined the game')

    def leaveGame(self):
        user = self.rawData.split(': ')[1].split(' left the game')[0]
        self.webhook.send(f':x: **{user}** left the game')
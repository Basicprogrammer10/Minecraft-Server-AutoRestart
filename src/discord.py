import requests
import json

class embed():
    def __init__(self, title, desc, color, footer = ''):
        self.title = title
        self.desc = desc
        self.color = int(color, 16)
        self.footer = footer


class webhook():
    def __init__(self, hookUri, doSend = True):
        self.hookUri = hookUri
        self.doSend = doSend
        self.data = json.loads(requests.get(hookUri).text) if doSend else None
        self.hookName = None

    def name(self, setName = None):
        if not self.doSend: return
        if setName == None:
            return self.data['name']
        self.hookName = setName

    def sendText(self, text):
        """Send Text"""
        if not self.doSend: return
        data = {"content": str(text)}
        if self.hookName != None: data['username'] = self.hookName
        r = requests.post(self.hookUri, json = data)
        return (r.status_code, r.text)

    def send(self, data):
        """Send text or an embed"""
        if not self.doSend: return

        # If Data just a string
        if isinstance(data, str):
            return self.sendText(data)

        # If data is an instance of embed
        if isinstance(data, embed):
            data = {"embeds": [{"title": data.title,"description": data.desc,"color": data.color,"footer": {"text": data.footer}}]}
            if self.hookName != None: data['username'] = self.hookName
            r = requests.post(self.hookUri, json = data)
            return (r.status_code, r.text)

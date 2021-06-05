import requests

class embed():
    def __init__(self, title, desc, color, footer = ''):
        self.title = title
        self.desc = desc
        self.color = int(color, 16)
        self.footer = footer


class webhook():
    def __init__(self, hookUri):
        self.hookUri = hookUri

    def sendText(self, text):
        """Send Text"""
        r = requests.post(self.hookUri, data = { "content": str(text) })
        return (r.status_code, r.text)

    def send(self, data):
        """Send text or an embed"""
        # If Data just a string
        if isinstance(data, str):
            return self.sendText(data)

        # If data is an instance of embed
        if isinstance(data, embed):
            r = requests.post(self.hookUri, json = {"embeds": [{"title": data.title,"description": data.desc,"color": data.color,"footer": {"text": data.footer}}]})
            return (r.status_code, r.text)

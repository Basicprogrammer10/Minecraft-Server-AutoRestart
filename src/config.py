import re

import common

class config:
    def __init__(self, configFile):
        self.configFile = configFile

    def read(self):
        common.debugPrint('Config', 'Parseing Config File', 'cyan')
        data = open(self.configFile, 'r').read().split('\n')
        final = {}
        for i in data:
            working = i.split('=')
            try:
                working[0] = working[0].replace(' ', '')

                typesParseing = working[1].replace(' ', '').lower()
                if typesParseing.isnumeric():
                    working[1] = int(typesParseing)
                elif typesParseing == 'true' or typesParseing == 'false':
                    working[1] = True if typesParseing == 'true' else False
                elif typesParseing == 'none':
                    working[1] = None
                else:
                    working[1] = re.search(r'".*"', working[1]).group().replace('"', '')
            except: pass
            if len(working[0]) >= 3 and working[0][0] != '#':final[working[0]] = working[1]
        common.debugPrint('Config', 'Config File Parsed Successfully', 'green')
        self.configFileData = final

    def get(self, item, fallback = None):
        if item in self.configFileData:
            return self.configFileData[item]
        return fallback 

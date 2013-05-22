"""
cleverbot.py - Willie Cleverbot Module
Copyright 2013 Anthony Brown - bui@bui.pm
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from hashlib import md5
from willie import web


class Cleverbot():
    def __init__(self):
        self.svars = {'start': 'y', 'icognoid': 'wsf', 'fno': '0',
                      'sub': 'Say', 'islearning': '1', 'cleanslate': 'false'}

    def think(self, thought):
        self.svars['stimulus'] = thought
        postdata = web.urlencode(self.svars)
        postdata += '&icognocheck=' + md5(postdata[9:29]).hexdigest()
        response = web.post('http://www.cleverbot.com/webservicemin', postdata).read().split('\r')

        self.svars['sessionid'] = response[1]
        self.svars['logurl'] = response[2]
        self.svars['vText8'] = response[3]
        self.svars['vText7'] = response[4]
        self.svars['vText6'] = response[5]
        self.svars['vText5'] = response[6]
        self.svars['vText4'] = response[7]
        self.svars['vText3'] = response[8]
        self.svars['vText2'] = response[9]
        self.svars['prevref'] = response[10]
        self.svars['emotionalhistory'] = response[12]
        self.svars['ttsLocMP3'] = response[13]
        self.svars['ttsLocTXT'] = response[14]
        self.svars['ttsLocTXT3'] = response[15]
        self.svars['ttsText'] = response[16]
        self.svars['lineRef'] = response[17]
        self.svars['lineURL'] = response[18]
        self.svars['linePOST'] = response[19]
        self.svars['lineChoices'] = response[20]
        self.svars['lineChoicesAbbrev'] = response[21]
        self.svars['typingData'] = response[22]
        self.svars['divert'] = response[23]

        return self.svars['ttsText']


# TODO: Let each user have their own cleverbot session
cleverbot = Cleverbot()

def cleverbot_think(willie, trigger):
    """Get Cleverbot to think about a thought"""
    thought = trigger.group(2)
    if not thought:
        return # TODO: Implement the "think for me" thingy

    response = cleverbot.think(thought)
    willie.reply(response)


cleverbot_think.commands = ['cb', 'cbot', 'cleverbot', 'think']
cleverbot_think.rule = '[Cc]leverbot[,:]? ()(.*)'
cleverbot_think.example = 'Cleverbot, you have beautiful eyes.'

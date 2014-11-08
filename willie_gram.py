from willie import module
import urllib.request
import json

@module.commands('anagram')
@priority('low')
def anagram(bot, trigger):
    try:
        url = "http://www.anagramica.com/best/:" + trigger
        data = urllib.request.urlopen(url).read().decode("utf-8")
        result = json.loads(data)
        bot.say(result.get("best")[0])
    except Exception as e:
        bot.say('Sorry, I couldn\'t make an anagram out of that.')
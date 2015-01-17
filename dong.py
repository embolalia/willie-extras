import willie
import random
import time

CONFIG={ 'timeout': {'start':60,'end':120} }
TIMEOUTS = {}
NSFW_LEVELS = {}

class Walkerrandom:
  """ Walker's alias method for random objects with different probablities
      Taken from http://code.activestate.com/recipes/576564-walkers-alias-method-for-random-objects-with-diffe/
  """

  def __init__( self, weights, keys=None ):
    """ builds the Walker tables prob and inx for calls to random().
        The weights (a list or tuple or iterable) can be in any order;
        they need not sum to 1.
    """
    self.n = sum(weights)
    self.keys = keys
    self.weightedlist = []
    for i in range(0, len(weights)):
        for _ in range(0,weights[i]):
            self.weightedlist.append(keys[i])
  def random( self ):
    j = random.randint( 0, self.n - 1 )  # or low bits of u
    return self.weightedlist[j]


class Component():
    ''' describes the random components
        the odds are actualy a weighted average '''
    def __init__(self, shape, text, odds, special=None):
        self.shape = shape
        self.text = text
        self.odds = odds
        self.special = special

class NSFW_Info():
    ''' Tracks the nsfw level of a room. Tracks the next time it is allowed
        to change '''
    MAX_LEVEL=4
    def __init__(self):
        ''' set a default level '''
        self.timeout = time.time() + 120
        self.level = 3
    def increase(self):
        if self.level < NSFW_Info.MAX_LEVEL and time.time() - self.timeout > 0:
            self.level += 1
            self.timeout = time.time() + 3600
            return True
        return False
    def decrease(self):
        if self.level > 0:
            self.level -= 1
            return True
        return False

class DongObject():
    def __init__(self, wnut, wshaft, wfore, wtip, wjizz):
        ''' create the dong, gen the size '''
        self.nut= wnut.random()
        self.shaft = wshaft.random()
        self.shaft_size = 0
        if len(self.shaft.shape) > 0:
            self.shaft_size = random.randint(0,12/len(self.shaft.shape))
        self.fore = wfore.random()
        self.tip = wtip.random()
        self.jizz = wjizz.random()
        self.has_jizz = random.random > 0.90
        self.jizz_size = 0
        if len(self.jizz.shape) > 0 and self.has_jizz:
            self.jizz_size = random.randint(1,6)
        self.dongspecials = ''
        self.dongspecialtext = []
        for part in [self.nut, self.shaft, self.fore, self.tip, self.jizz]:
            if part.text is not None and len(part.text) > 0:
                self.dongspecialtext.append(part.text)
    def add_special(self,text):
        self.dongspecialtext.append(text)
    def get_specials(self):
        return ' '.join(self.dongspecialtext)
    def get_shaft(self):
        output = ''
        for _ in range(0,self.shaft_size):
            output += self.shaft.shape
        return output
    def __str__(self):
        output = self.nut.shape
        output += self.get_shaft()
        output += self.fore.shape
        output += self.tip.shape
        for _ in range(0,self.jizz_size):
            output += self.jizz.shape
        output += self.dongspecials
        output += ' '
        output += self.get_specials()
        return output
    def __repr__(self):
        return self.__str__()


class BaseLevel():
    def __init__(self):
        self.nut = []
        self.shaft = []
        self.fore = []
        self.tip = []
        self.jizz = []
    def build_table(self,table):
        mylist = []
        for e in table:
            mylist.append(e.odds)
        return Walkerrandom(mylist,table)
    def build_tables(self):
        self.wnut = self.build_table(self.nut)
        self.wshaft = self.build_table(self.shaft)
        self.wfore = self.build_table(self.fore)
        self.wtip = self.build_table(self.tip)
        self.wjizz = self.build_table(self.jizz)

    def get_stack(self):
        return DongObject(self.wnut, self.wshaft, self.wfore, self.wtip,
                self.wjizz)

class Level0(BaseLevel):
    def __init__(self):
        self.nut = [Component('','',1)]
        self.nut.append(Component('=^..^=','kitty cat',1))
        self.nut.append(Component('<`)))><','fishy fishy fish',1))
        self.nut.append(Component('c[]','coffee',1))
        self.nut.append(Component('<:3 )~~~~','a mouse!',1))
        self.shaft = [Component('','',1)]
        self.fore= [Component('','',1)]
        self.tip = [Component('','',1)]
        self.jizz = [Component('','',1)]
        self.build_tables()

class Level1(BaseLevel):
    def __init__(self):
        self.nut = [Component('8','',1)]
        self.shaft = [Component('=','',1)]
        self.fore = [Component('','',1)]
        self.tip = [Component('D','',1)]
        self.jizz = [Component('','',1)]
        self.build_tables()
class Level2(BaseLevel):
    def __init__(self):
        self.nut = [Component('8','',1)]
        self.shaft = [Component('=','',1)]
        self.fore = [Component('','',1)]
        self.tip = [Component('D','',1)]
        self.jizz = [Component('','',1)]
        self.build_tables()
    def get_stack(self):
        d = DongObject(self.wnut, self.wshaft, self.wfore, self.wtip,
                self.wjizz)
        if d.shaft_size >= 12:
            d.add_special('MASTER CYLINDER')
        elif d.shaft_size == 1:
            d.add_special('SHORTSTACK')
        return d
class Level3(BaseLevel):
    def __init__(self):
        self.nut = [Component('8','',20)]
        self.nut.append(Component(':','WINTERIZED',1))
        self.nut.append(Component('o','ARMSTRONG\'D',1))
        self.shaft = [Component('=','',20)]
        self.shaft.append(Component('-','NOODLE',1))
        self.fore = [Component('','',1)]
        self.tip = [Component('D','',1)]
        self.jizz = [Component('','',1)]
        self.build_tables()
    def get_stack(self):
        d = DongObject(self.wnut, self.wshaft, self.wfore, self.wtip,
                self.wjizz)
        if d.shaft_size >= 12:
            d.add_special('MASTER CYLINDER')
        elif d.shaft_size == 1:
            d.add_special('SHORTSTACK')
        elif d.shaft_size == 0:
            d.add_special('NUB')
        return d

class Level4(BaseLevel):
    def __init__(self):
        self.nut = [Component('8','',50)]
        self.nut.append(Component(':','WINTERIZED',1))
        self.nut.append(Component('o','ARMSTRONG\'D',1))
        self.nut.append(Component('.','WINTERIZE\'D ARMSTRONG\'D',1))
        self.nut.append(Component('B','GRAPEFRUITS',1))
        self.nut.append(Component(' ','VASECTOMY\'D',1))
        self.shaft = [Component('=','',50)]
        self.shaft.append(Component('-','NOODLE',1))
        self.shaft.append(Component('~','COMPRESSION',1))
        self.shaft.append(Component('/\\','ACCORDION',1))
        self.shaft.append(Component('^','STUDDED',1))
        self.shaft.append(Component(')','RIBBED',1))
        self.fore = [Component('','',100)]
        self.fore.append(Component(')','CLIPPED',1))
        self.fore.append(Component('|||','TURTLENECK',1))
        self.tip = [Component('D','',1000)]
        self.tip.append(Component('-','UNICORN',1))
        self.tip.append(Component('G','PEIRCED',5))
        self.tip.append(Component('Q','LEAKER',5))
        self.tip.append(Component('3','DICKBUTT',5))
        self.jizz = [Component('','',200)]
        self.jizz.append(Component('~','',10))
        self.jizz.append(Component('~','SCHNOODLE',1))
        self.jizz.append(Component('~ ','SPUTTER',1))
        self.build_tables()

    def get_stack(self):
        d = DongObject(self.wnut, self.wshaft, self.wfore, self.wtip,
                self.wjizz)
        if d.jizz_size >= 6:
            d.add_special('BIG SHOOTER')
        if d.shaft_size >= 12:
            d.add_special('MASTER CYLINDER')
        elif d.shaft_size == 1:
            d.add_special('SHORTSTACK')
        elif d.shaft_size == 0:
            d.add_special('NUB')

        if d.jizz_size == 0 and random.random() > 0.99:
            # copy the shaft but not nut
            d.dongspecials = d.get_shaft() + d.nut.shape
            d.add_special("DOCKING!")
        elif random.random() > 0.99:
            d.dongspecials = 'C' + d.get_shaft() + d.nut.shape
            d.add_special("SWORDFIGHT!")
        return d

LEVELS = [ Level0(), Level1(), Level2(), Level3(), Level4() ]

@willie.module.commands('dong')
def dongbot(bot, trigger):
    """Print out some dongs. Usage .dong"""
    bot.say("Creating shaft size comparisons...")
    if not trigger.sender in TIMEOUTS:
        TIMEOUTS[trigger.sender]=0
    if not trigger.sender in NSFW_LEVELS:
        NSFW_LEVELS[trigger.sender] = NSFW_Info()
    if trigger.sender.startswith('#'):
        if time.time() - TIMEOUTS[trigger.sender] < 0:
           bot.say('%s is a dong'%trigger.nick)
           return
        TIMEOUTS[trigger.sender] = time.time() + random.randint(
                CONFIG['timeout']['start'], CONFIG['timeout']['end'])
        # get the components for the run
        users = bot.privileges[trigger.sender]
        for u in users:
            d = LEVELS[ NSFW_LEVELS[trigger.sender].level ].get_stack()
            bot.say('%s: %s'%(u, d))

    else:
        bot.say('You are indeed a dong')

@willie.module.commands('cockblock')
def cockbock(bot, trigger):
    """Stop writing dongs for one to two hours"""
    amount = random.randint(3600,7200)
    TIMEOUTS[trigger.sender] = time.time() + amount
    bot.say('Stopping dongs for %d minutes'%(int(amount/60)))

@willie.module.commands('nsfwdongs')
def nsfwdongs(bot, trigger):
    """ Increse or Decrease the rudeness of the dongs. .nsfwdongs more,
        .nsfwdongs less. Or, in a private chat, .nsfwdongs less #chatname. """
    if not trigger.group(2):
        bot.say("more, or less?")
        return
    commands = trigger.group(2).split()
    if not trigger.sender.startswith('#') and trigger.group(2) == 'more':
        bot.say("You need to say this in the public chat... perv.")
        return
    elif not trigger.sender.startswith('#') and trigger.group(2) == 'less':
        bot.say("Which chat? .nsfwdongs less #chatname")
        return
    elif trigger.group(2) == 'more' and trigger.sender in NSFW_LEVELS:
        if ( NSFW_LEVELS[trigger.sender].increase() ):
            bot.say("PREPARE FOR RUDNESS")
        else:
            bot.say("No can do")
    elif (trigger.group(2) == 'less' and trigger.sender.startswith('#') and
            trigger.sender in NSFW_LEVELS):
        if ( NSFW_LEVELS[trigger.sender].decrease() ):
            bot.say("Finally someone sane")
        else:
            bot.say("This is as inoffensive as it gets")
    elif (commands[0] == 'less' and len(commands) > 1):
        if commands[1] in NSFW_LEVELS:
            if NSFW_LEVELS[commands[1]].decrease():
                bot.say("Rudeness silently lowered in %s"%commands[1])
            else:
                bot.say("That's as nice as it gets, sorry")
        else:
            bot.say("%s is not a chat I know"%commands[1])
    else:
        bot.say("Sorry. Didn't get that")

@willie.module.commands('donglevel')
def donglevel(bot, trigger):
    """ Check the nsfw level of the current room """
    if trigger.sender in NSFW_LEVELS:
        bot.say("%s is at rudeness level %d/%d"%(trigger.sender,
            NSFW_LEVELS[trigger.sender].level,NSFW_Info.MAX_LEVEL))
    else:
        bot.say("Bot not donging in chat '%s'."%trigger.sender)



@willie.module.commands('dongwhen','dongwait')
def dongwait(bot, trigger):
    """ Check how long we must wait for the next donging """
    if trigger.sender not in TIMEOUTS:
        bot.say("Get started any time!")
        return
    if time.time() - TIMEOUTS[trigger.sender] > 0:
        bot.say("Any time you like.")
        return
    wait = int(TIMEOUTS[trigger.sender] - time.time())/60
    if wait == 1 or wait == 0:
        bot.say ("You can in 1 minute")
    else:
        bot.say ("You can in %d minutes"%(wait))

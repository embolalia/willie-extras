import willie
import random
import time
from bs4 import BeautifulSoup
import urllib2
import Queue


SCORES = {}
PHASE_LENGTH = 30

def configure(config):
    config.add_option('movietriv', 'movielist_file', 
        'location of imdb_ids and titles')

class movie():
    def __init__(self, title, imdb_id):
        self.title = title.lower()
        self.imdb_id = imdb_id
    def get_quote(self):
        response = urllib2.urlopen(
                'http://www.imdb.com/title/%s/quotes'%self.imdb_id)
        html = response.read()

        soup = BeautifulSoup(html)

        quotes = soup.find_all(class_='sodatext')
        index = random.randint(0, len(quotes))
        return random.choice(quotes).get_text().strip()


class guess():
    def __init__(self, nick, guess):
        self.nick = nick
        self.guess = guess

class quote_game():
    """ A Queue is used to send the thread guesses
        The game is run in the thread so it can schedule tasks.
        The thread is encapsulated in a game object, so there is potentially
        one thread for each room the game is being run in
    """
    def __init__(self, bot, room):
        self.movies = []
        self.is_running = False
        self.q = Queue()
        self.t = None
        self.current_movie = None
        self.bot = bot
        self.room = room
        self.next_phase= 0
        self.phase = 0
        self.load_file(bot.config.movietriv.movielist_file)
    def add_movie(self, title, imdb_id):
        self.movies.append(movie(title, imdb_id))
    def give_points(self, nick):
        if nick in SCORES:
            SCORES[nick] += 5
        else:
            SCORES[nick] = 5
    def next_movie(self):
        if self.current_movie is not None:
            self.bot.msg(room, "Correct answer was "
                   "%s."%self.current_movie.title)
        self.next_phase = time.time() + PHASE_LENGTH
        self.phase = 0
        self.current_movie = random.choice(self.movies)
    def load_file(self, f):
        with open(f) as thefile:
            for line in thefile.readlines():
                words = line.split()
                self.add_movie(' '.join(words[1:]), words[0])
    def make_guess(self,nick,guess):
        self.q.put( guess(nick, guess) )
    def start_game(self,bot):
        """ Start the game thread """
        def run_game(bot):
            while(self.is_running):
                go_next = False
                while not q.empty():
                    guess = q.get()
                    # Allows more than one person to get it right
                    # provided they wrote it in the last second with the
                    # other person. But only the first gets points.
                    if guess.guess == self.current_movie.title:
                        bot.say("Correct, %s"%guess.nick)
                        if not go_next:
                            bot.say("Points awarded to %s."%guess.nick)
                            self.give_points(guess.nick)
                        go_next = True
                # do scheduled tasks, if needed
                if go_next:
                    self.next_movie()
                elif time.time() - self.next_phase > 0:
                    # if phase > 2, give another hint.
                    # otherwise, move to the next movie.
                    if self.phase < 2:
                        self.phase += 1
                        bot.msg(room, "Hint #%d"%self.phase)
                        bot.msg(room, self.current_movie.get_quote())
                    else:
                        bot.msg(room, "Time's up!")
                        self.next_movie()
                # sleep
                time.sleep(1)

        if self.is_running:
            # this shouldn't run, but just in case...
            bot.say("game is already running!")
            return
        self.t = threading.Thread(target=run_game, args=(bot,))
        self.t.start()

    def stop_game(self):
        self.is_running = False
        self.t.join()




@willie.module.commands('trivstart')
def start(bot, trigger):
    """ Start a game of Movie Quote Trivia """
    if game.is_running:
        bot.say("Game is already running. Pay attention!")
    else:
        game.start_game(bot)

@willie.module.commands('guess','g')
def guess(bot, trigger):
    """ Make a guess at the answer to the movie trivia """
    pass

@willie.module.commands('trivstop')
def stop(bot, trigger):
    """ stop a game of movie quote trivia """
    bot.say("Stopping game. This may take a moment")
    self.game.stop_game()


@willie.module.commands('trivscore')
def getscore(bot, trigger):
    """ Get the points for yourself. """
    if trigger.nick in SCORES:
        bot.say("Score for %s is %d"%(trigger.nick, SCORES[trigger.nick]))
    else:
        bot.say("%s: I don't know you, so I guess your score is "
            "0."%trigger.nick)

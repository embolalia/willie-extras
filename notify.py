# vim: tabstop=4 softtabstop=4 shiftwidth=4 textwidth=80 smarttab expandtab
"""
notify.py - Simple Willie notfication plugin
Copyright 2014, Moises Silva <moises.silva@gmail.com>
Licensed under the Eiffel Forum License 2.

http://willie.dfbta.net
"""
import os
import errno
import zmq
import willie.module

zsocket = None

def configure(config):
    config.add_option('notify', 'server_address', 'Address to read notifications from')

def setup(bot):
    global zsocket
    # create a subscribe socket and accept all events
    c = zmq.Context()
    zsocket = c.socket(zmq.SUB)
    zsocket.setsockopt(zmq.SUBSCRIBE, '')
    zsocket.connect(bot.config.notify.server_address)

def shutdown(bot):
    if zsocket:
        zsocket.close()

@willie.module.interval(5)
def check_notifications(bot):
    while True:
        try:
            msg = zsocket.recv(zmq.NOBLOCK)
        except zmq.ZMQError, e:
            if e.errno == errno.EAGAIN:
                return
            raise
        for c in bot.channels:
            c = str(c)
            bot.msg(c, msg)

# coding=utf-8
""" 
memdump.py - Willie Memdump Module
Copyright 2014, Harri Berglund
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net

Remember: With great power comes great responsibility.

"""

import willie.module

MAX_LINES = 5


def configure(config):
    if config.option('Configure memdump module', False):
        config.add_section('memdump')
        config.add_list(
            'memdump', 
            'channel_whitelist', 
            'List channels on which the `memdump` command shall be enabled.', 
            'Add channel (leave empty to stop):', 
        )
        config.interactive_add(
            'memdump', 
            'max_lines', 
            'Maximum number of lines to send via PRIVMSG', 
            MAX_LINES, 
        )


def setup(bot):
    if not bot.config.has_section('memdump'):
        bot.config.add_section('memdump')
        bot.config.memdump.channel_whitelist = []
        bot.config.memdump.max_lines = MAX_LINES


def _memdump(bot, key, attr):
    error = False
    
    try:
        if not attr:
            result = repr(bot.memory[key])
        else:
            result = repr(getattr(bot.memory[key], attr))
    except KeyError:
        error = True
        result = "bot.memory['%s'] does not exist" % key
    except AttributeError:
        error = True
        result = "bot.memory['%s'] has no attribute '%s'" % (key, attr)
    
    return (error, result)


# workaround to prepend `nick: ` only when _not_ replying to a private message
def _reply(bot, trigger, message, max_lines=1):
    if not trigger.is_privmsg:
        message = '%s: %s' % (trigger.nick, message)
    bot.msg(trigger.sender, message, max_lines)


@willie.module.commands('memdump')
@willie.module.example('.memdump last_seen_url')
@willie.module.priority('low')
def memdump_command(bot, trigger):
    
    """Show a string representation of an entry in the bot's memory."""
    
    if not trigger.admin:
        message = 'That command is only available to administrators.'
        _reply(bot, trigger, message)
        return
    if not trigger.is_privmsg:
        channel = trigger.sender.lower()
        if channel not in bot.config.memdump.get_list('channel_whitelist'):
            bot.reply('That command is not allowed on this channel.')
            return
    
    try:
        max_lines = int(bot.config.memdump.max_lines)
    except ValueError:
        max_lines = MAX_LINES
    write_to_stdout = False
    
    text = trigger.group(2) or ''
    if text.startswith('--stdout'):
        write_to_stdout = True
        text = text[8:].lstrip()
    
    key, separator, attr = text.partition(' ')
    if not key:
        keys = sorted(bot.memory.keys())
        usage_instructions = (
            'Usage: .memdump [--stdout] <key> [<attribute>] | '
            'Keys: %s' % ', '.join(keys)
        )
        _reply(bot, trigger, usage_instructions, max_lines)
        return
    attr = attr.strip()
    
    error, result = _memdump(bot, key, attr)
    if write_to_stdout and not error:
        print('%s\n' % result)
    else:
        _reply(bot, trigger, result, max_lines)

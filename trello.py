# -*- coding: utf-8 -*-
"""
willie-trello.py - Enhanced Trello links
Licensed under the GNU GPLv3
Copyright (C) 2015 Kieran Peckett
"""
import willie.module
import requests
import time
import re

def setup(bot):
	regex = re.compile(r".*\bhttps?://trello\.com/c/(\w+).*")
	if not bot.memory.contains('url_callbacks'):
		bot.memory['url_callbacks'] = {regex: showTrelloInfo}
	else:
		exclude = bot.memory['url_callbacks']
		exclude[regex] = showTrelloInfo
		bot.memory['url_callbacks'] = exclude

@willie.module.rule(r".*https?://trello\.com/c/(\w+).*")
def showTrelloInfo(bot,trigger,found_match=None):
	"""Shows info about a card on Trello"""
	match = found_match or trigger
	card_id = match.group(1)
	url = "https://api.trello.com/1/card/" + card_id + "?fields=name,closed,desc,due,shortUrl"
	response = requests.get(url)
	if response.text == "unauthorized card permission requested":
		bot.say("Private Trello Card")
	else:
		data = response.json()
		output = data["name"] # Add name of card
		# Add first 50 chars or less of description
		if len(data["desc"]) > 50:
			output += " | " + data["desc"][0:75] + u"…" # Add ellipsis at end
		elif data["desc"] == "":
			output += " |  No Description"
		else:
			output += " | " + data["desc"]
		if data["due"] == None:
			output += " | No Due Date"
		else:
			due_date = data["due"][0:10]
			output += " | Due: " + due_date
		output += " | " + data["shortUrl"]
		bot.say(output)

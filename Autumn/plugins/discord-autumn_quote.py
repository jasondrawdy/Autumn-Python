#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_quote.py - Shows a quote to the user.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module handles the selection and displaying of a quote.
#-------------------------------------------------------------------------
import os
import random
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        filepath = "plugins/quotes/"
        file = filepath + "quotes.txt"
        if os.path.exists(filepath):
            if os.path.exists(file):
                with open(file, 'r') as f:
                    lines = f.read().splitlines()
                    number = random.randint(0, len(lines) - 1)
                    quote = lines[number]
                    await self.message.channel.send(quote)
            else:
                await self.message.channel.send("I don't have any quotes to quote.")
        else:
            await self.message.channel.send("I don't have any quotes to quote.")

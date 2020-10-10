#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_hi.py - Sends a friendly hello to the sender.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends a hello to a user who originally greeted Autumn.
#-------------------------------------------------------------------------
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        message = "Hi, " + self.message.author.mention + "! :heart:"
        await self.message.channel.send(message)

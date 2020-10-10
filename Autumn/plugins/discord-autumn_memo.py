#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_memo.py - Sends a message to a channel and @'s everyone.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module mentions @everyone in a channel with a specified message.
#-------------------------------------------------------------------------
import asyncio
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        author = str(self.message.author)
        channel = self.message.channel
        if author in self.bot.friends:
            if len(args[0]) >= 2:
                try:
                    sendToSystem = False
                    guild = self.message.author.guild
                    message = "@everyone " + ' '.join(args[0][1:])
                    try:
                        if args[0][1].find('#'):
                            channelID = args[0][1].split('#')[1].split('>')[0]
                            for c in guild.text_channels:
                                if str(c.id) == channelID:
                                    message = "@everyone " + ' '.join(args[0][2:])
                                    await c.send(message)
                    except: sendToSystem = True # The memo is for the system channel.
                    if sendToSystem:
                        if guild.system_channel is not None:
                            await guild.system_channel.send(message)
                        else:
                            await channel.send("There isn't a system channel to announce the memo in.")
                except:
                    await channel.send("I can't send a memo in a private conversation.")
            else:
                await channel.send("There should be something to send! Please enter a message.")
        else:
            await channel.send("Only my master or a server owner can issue a memo.")

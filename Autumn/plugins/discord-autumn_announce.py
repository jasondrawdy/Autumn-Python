#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_announce.py - Makes an announcement in a channel.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Creates an announcement in a specified server channel.
# -------------------------------------------------------------------------
import asyncio
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        author = str(self.message.author)
        channel = self.message.channel
        if author is self.bot.botMaster:
            if len(args[0]) >= 2:
                try:
                    message = "**ANNOUNCEMENT**: " + ' '.join(args[0][1:])
                    for guild in self.client.guilds:
                        if guild.system_channel is not None:
                            await guild.system_channel.send(message)
                        else:
                            try:
                                await guild.text_channels[0].send(message)
                            except:
                                await channel.send("I was unable to make the announcement on " + str(guild.name) + ".")
                except:
                    await channel.send("I'm unable to make the announcement at the moment.")
            else:
                await channel.send("There should be something to send! Please enter a message.")
        else:
            await channel.send("Only my master or a server owner can issue a memo.")

#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_dm.py - Sends a private message to the user.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends a private message to a user.
# -------------------------------------------------------------------------
import discord
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        sender = self.message.channel
        if str(self.message.author) in self.bot.friends:
            if len(args[0]) >= 3:
                if "@" in args[0][1]:
                    try:
                        sent = False
                        user = args[0][1].split('!')[1].split('>')[0]
                        message = ' '.join(args[0][2:])
                        for guild in self.client.guilds:
                            if sent:
                                break
                            for member in guild.members:
                                if user in str(member.id):
                                    await member.send(message)
                                    await sender.send(self.message.author.mention + ", I've sent the DM for you!")
                                    sent = True
                                    break
                                else:
                                    pass
                    except: await sender.send("The user could not be messaged at this time.")
                else:
                    await sender.send("The user should be mentionable.")
            else:
                await self.usage(sender)
        else:
            await sender.send("Only my master or a server administrator can send a DM.")

    async def usage(self, sender):
        await sender.send("**USAGE**: bot.dm @*{user}* *{message}*")

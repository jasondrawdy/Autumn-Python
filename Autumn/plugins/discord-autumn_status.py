#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_status.py - Changes the current status of the bot.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module handles the configuration of the bot's current status.
# -------------------------------------------------------------------------
import discord
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        if str(self.message.author) == self.bot.botMaster:
            if len(args[0]) < 1:
                await self.message.channel.send("Enter a status for me to use!")
            else:
                message = ' '.join(args[0][1:])
                status = discord.Activity(type=discord.ActivityType.watching, name=message)
                await self.client.change_presence(activity=status)
                await self.message.channel.send(self.message.author.mention + ", my status has been updated!")
        else:
            await self.message.channel.send("Only my master can change my status, silly.")

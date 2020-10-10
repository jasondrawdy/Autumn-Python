#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_friends.py - Slide into friend's DMs.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module is a test message function.
#-------------------------------------------------------------------------
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        found = {}
        for friend in self.bot.friends:
            try:
                if not friend in found and not self.bot.friends[friend] == "Self":
                    for guild in self.client.guilds:
                        if not friend in found:
                            for member in guild.members:
                                if str(member) == friend:
                                    found[friend] = "found"
                                    await member.send("Shhh.. :shushing_face: \n\nI'm just sliding into your *DM* to test some stuff...")
                                    print("Messaged: " + friend)
                                    break
            except: pass
        if len(found) > 0:
            if len(found) == len(self.bot.friends):
                await self.message.channel.send("All of my friends have been notified!")
            else:
                count = len(found)
                await self.message.channel.send("Only " + str(count) + " of my friends have been notified...")
        else:
            await self.message.channel.send("My friends couldn't be notified.")

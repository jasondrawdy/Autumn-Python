#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_kick.py - Kicks a user from the server.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module removes a specified user from the Discord server.
# -------------------------------------------------------------------------
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        sender = str(self.message.author)
        if sender == self.bot.botNick or sender in self.bot.friends:
            if len(args[0]) > 2:
                await self.message.channel.send("The command only requires a name/mention as a parameter.")
            elif len(args[0]) == 2:
                user = args[0][1]
                if not user.find('<@'):
                    try:
                        me = False
                        kicked = False
                        id = user.split('@')[1].split('>')[0]
                        id = id.replace('!', '')
                        guild = self.message.author.guild
                        for member in guild.members:
                            user = str(member.id)
                            if user == id:
                                name = member.display_name
                                if not name.find('Autumn'):
                                    await self.message.channel.send("I can't kick myself from the server, silly.")
                                    me = True
                                else:
                                    await member.kick()
                                    kicked = True
                                    break
                        if not me:
                            if not kicked:
                                await self.message.channel.send("A user with that name could not be found.")
                            else:
                                await self.message.channel.send(member.mention + " has been kicked from the server!")
                    except: pass
                    #print(user)
                else:
                    await self.message.channel.send("That's not a real person!")
            else:
                await self.message.channel.send("The command requires a valid name or mention to function.")
        else:
            await self.message.channel.send("Only an administrator can kick people from a server.")

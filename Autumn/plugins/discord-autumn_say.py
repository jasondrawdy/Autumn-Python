#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_say.py - Sends a test message to a channel.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends a test message to a channel.
# -------------------------------------------------------------------------
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        if str(self.message.author) == self.bot.botMaster:
            if len(args[0]) > 3:
                sent = False
                server = ""
                channel = ""
                comment = ' '.join(args[0][3:])
                index = 0
                for arg in args[0]:
                    if str(self.message.author) in arg:
                        pass
                    else:
                        if "#" in arg:
                            server += "x"
                            server = ''.join(server[0:len(server) - 2])
                            channel = arg.split('#')[1].split('>')[0]
                            comment = ' '.join(args[0][index+1:])
                            break
                        server += arg + " "
                    index += 1
                for guild in self.client.guilds:
                    if server in guild.name:
                        channels = guild.text_channels
                        for chan in channels:
                            if channel in str(chan.id) or channel in chan.name:
                                channel = chan.name
                                await chan.send(comment)
                                sent = True
                            else:pass
                    else:pass
                if sent:
                    await self.message.channel.send("I sent the message to #" + channel + " on " + server + "!")
                else:
                    await self.message.channel.send("I couldn't send a message because either the server or channel doesn't exist.")
            else:
                await self.usage()
        else:
            await self.message.channel.send("Only my master can make me say something... :blush:")
    async def usage(self):
        message = "**Usage**: bot.say {*server*} {*#channel*} {*message*}"
        await self.message.channel.send(message)

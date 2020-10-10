#!/usr/bin/python
#-------------------------------------------------------------------------
# handler.py - Handles all events for Autumn.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Autumn is a simple Discord bot meant to aid in the moderating of a single
# server under a single bot master and with minimal interaction/commands.
#-------------------------------------------------------------------------

#=======================================
# Imports
#=======================================
import discord
import asyncio
import random
from modules import messages

#=======================================
# Variables
#=======================================
# Globals
null = -1
autumn = null
client = discord.AutoShardedClient()

class Handler(object):
    def __init__(self, bot, path="/plugins"):
        global autumn
        autumn = bot
        autumn.client = client
        self.bot = autumn
        self.path = path

    @staticmethod
    @client.event
    async def on_member_join(member):
        info = ":information_source:  **IMPORTANT**: Please read the rules and f.a.q if applicable and remember to respect other members. Thank you! :heart_exclamation:"
        message = "Hello, $MENTION$. Welcome to $SERVER$! We hope you enjoy your stay in the community and also please remember to be nice to the other members that are connected.\n"\
                  "You can access my commands by typing — **user.** — and you can access <@!693328126457151538>'s commands by" \
                  "typing the prefix — **bot.** — and then the name of the command. Again, remember to be respectful of others!\n"\
                  "If you have any questions, comments, or concerns you can message either <@!530648978052874247> or **Gummo**.\n"\
                  "Have fun on the server! :pirate_flag:"
        guild = member.guild
        if guild.system_channel is not None:
            if guild.name == "Autumn Support" or guild.name == "Research":
                await guild.system_channel.send("Hi, " + member.mention + "! :heart:\n\n" + info)
            else:
                await guild.system_channel.send("Hi, " + member.mention + "! :heart:")
        else:
            pass

    @staticmethod
    @client.event
    async def on_ready():
        messages.printMessage('We have logged in as {0.user}'.format(autumn.client))
        messages.printMessage('Checking for guild information.')
        autumn.check_guild_info()

    @staticmethod
    @client.event
    async def on_reaction_add(reaction, user):
        def has_permission(message, user):
            roles = []
            for member in message.guild.members:
                if member.id == user.id:
                    roles = member.roles
                    break
                else:
                    pass
            if len(roles) > 0:
                for role in roles:
                    if role.permissions.administrator:
                        return True
                    else:
                        split = role.name.split(' ')
                        if split[0].lower() in autumn.roles:
                            return True
                        else:
                            pass
                return False
            else:
                return False

        if reaction.emoji == "❌":
            if user != autumn.client.user:
                if str(user) is autumn.botMaster or str(user) in autumn.friends or has_permission(reaction.message, user):
                    if reaction.message.author == autumn.client.user:
                        try: await reaction.message.delete()
                        except: pass
                else: pass
            else: pass
        else: pass

    @staticmethod
    @client.event
    async def on_message(message):
        await messages.processMessage(autumn, message)
        media = ["https://www.youtube.com/watch?", "https://youtu.be/"] # Typical links to react to.
        extensions = ['.jpg', '.png', '.gif', '.bmp', '.raw', '.tiff']
        should_post = False
        i = random.randint(0, 100)
        if i >= 51:
            should_post = True
        for item in media:
            if item in message.content.strip():
                if should_post:
                        number = random.randint(0, len(autumn.positive_reactions) - 1)
                        await message.add_reaction(autumn.positive_reactions[number])
        try:
            if str(message.author) in autumn.friends:
                count = len(str(message.attachments[0]))
                if count > 0:
                    for extension in extensions:
                        if extension in str(message.attachments[0]):
                            if should_post:
                                    number = random.randint(0, len(autumn.positive_reactions) - 1)
                                    await message.add_reaction(autumn.positive_reactions[number])
        except: pass

    async def watch_plugins(self, time=1):
        while True:
            self.bot.loadPlugins(self.path)
            await asyncio.sleep(time)  # Sleep the thread 200 ms.

    def start(self, bot):
        try:
            global autumn
            autumn = bot
            autumn.client = client
            self.bot = autumn
            self.bot.connected = True
            self.bot.client.run(self.bot.settings.api_key)
        except: pass

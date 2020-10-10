#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_help.py - Displays help information related to Autumn.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends help information related to Autumn.
# -------------------------------------------------------------------------
import discord
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        await display(self.bot, self.message)

async def display(bot, message):
    name = "a server that you currently reside"
    try:
        name = message.author.guild.name
    except:
        pass
    response = "Hello! My name is **Autumn** and I am a _shardless_ Discord bot developed by _Buddha#0029_ " \
              "in order to aid in the management of channels, displaying information, and for assisting server members " \
              "with common and uncommon tasks. Please check my posted information as well as any server memos that have " \
              "been posted before contacting an administrator. A list of my available commands can be found below:\n\n" \
              "**Important:** _Most if not all of these commands support NLP (natural language processing) thanks to IBM's Watson!_\n\n" \
              "**__Admin Commands__**\n" \
              "These commands are only available to a server administrator.\n" \
              "```" + bot.prefix + "memo ....... Displays a memo message to all users in a channel\n" \
              + bot.prefix + "dm ......... Sends a private message to a mentionable user\n" \
              + bot.prefix + "kick ....... Kicks a user from the server\n" \
              + bot.prefix + "ban ........ Bans a user from the server\n" \
              + bot.prefix + "say ........ Sends a message to a specified server and channel\n" \
              + bot.prefix + "settings ... Displays the server settings module for admins\n" \
              + bot.prefix + "announce ... Displays a memo message to all users in all servers (Bot master only)\n" \
              + bot.prefix + "status ..... Changes the display status for Autumn (Bot master only)```\n\n" \
              "**__Basic Commands__**\n" \
              "Commands that are available to all users in the server." \
              "```" + bot.prefix + "hi ......... Displays a greeting to the sender\n" \
              + bot.prefix + "roles ...... Establishes a role for the user if none\n" \
              + bot.prefix + "ping ....... Pings the user back after a request\n" \
              + bot.prefix + "math ....... Calculates a given equation (basic formulas only)\n" \
              + bot.prefix + "uptime ..... Displays the amount of time Autumn has been up\n" \
              + bot.prefix + "help ....... Displays detailed help information about Autumn```\n" \
              "**__Game Commands__**\n" \
              "```" + bot.prefix + "guess ...... Generates a random number for the player to guess```\n\n" \
              "If you need any further assistance with the server, channels, or how I operate, then please feel free " \
              "to reach out to _Buddha#0029_ or one of the admins for " + name + ". "\
              "Also, please remember to be kind and respectful of others as they have feelings too. Enjoy! :heart:"
    #embed = discord.Embed(title="Test Title", description="Test Description", color=0xea1e63)
    await message.author.send(response)#, embed=embed)

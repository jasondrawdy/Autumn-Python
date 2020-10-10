#!/usr/bin/python
# -------------------------------------------------------------------------
# commands.py - Handles all command logic for Autumn.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module controls all commands and their corresponding functionality.
# -------------------------------------------------------------------------
import discord
from modules import messages
from modules import utils
from modules import logging
from modules import commands

null = -1

class CommandBundle(object):
    def __init__(self, bot, message, prefix):
        self.bot = bot
        self.message = message
        self.prefix = prefix

def isCommand(bot, message):
    try:
        if message.content == "bot.restart":
            return commands.CommandBundle(bot, message, "bot.")
        elif message.content == "bot.help":
            return commands.CommandBundle(bot, message, "bot.")
        else:
            split = message.content.split(' ')[0]
            prefix = None
            count = len(bot.settings.guild_info)
            if count is not None:
                try:
                    for guild in bot.settings.guild_info:
                        if guild == str(message.author.guild.id):
                            prefix = bot.settings.guild_info[guild].guild_prefix
                            prefix = split[0:len(prefix)]
                            break
                except: pass

            if prefix is None:
                prefix = bot.prefix
                prefix = split[0:len(prefix)]
            if prefix == bot.prefix or prefix == bot.settings.guild_info[guild].guild_prefix or split[0:2] == "!!":
                bundle = commands.CommandBundle(bot, message, prefix)
                return bundle
    except: pass

async def processCommand(bundle):
    # Parse our command.
    args = bundle.message.content.split(" ")
    c = args[0]
    if bundle.prefix in c:
        c = c.replace(bundle.prefix, bundle.bot.prefix)

    # Restart the bot if the master says so.
    if c.lower() == "bot.restart":
        if str(bundle.message.author) == bundle.bot.botMaster:
            utils.restart_program()

    # Continue loading the plugin.
    command = bundle.bot.commands.get(c, null)
    if command != null:
        if isinstance(command, str):
            # print("Sending a reply...")
            # Reply to the user or channel
            await bundle.message.channel.send(command)
        else:
            # Create a new loader instance and run the plugin with args.
            try:
                name = args[0][len(bundle.prefix):].lower()
                args[0] = str(bundle.message.author)
                plugin = utils.Loader(bundle.bot, name, bundle.message, args)
                command.loader = plugin
                command.message = bundle.message
                await plugin.start()
            except Exception as error:
                bundle.message.channel.send(str(error))
                if logging.Logger.verbosityLevel >= logging.Verbosity.NONE:
                    messages.printMessage(str(error), messages.MessageType.EXCEPTION, True)

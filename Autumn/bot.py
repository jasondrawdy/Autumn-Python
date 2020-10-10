#!/usr/bin/python
#-------------------------------------------------------------------------
# bot.py - Encapsulation module for information pertaining to Autumn
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module controls all aspects of the bot itself such as its name and
# other information such as the commands and or the replies it uses.
#-------------------------------------------------------------------------

import os
import pickle
import discord
from pathlib import Path
from modules import utils
from modules import messages
from modules import logging
from modules.settings import Settings
from modules.guilds import GuildInfo
from datetime import datetime
from importlib import import_module
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

null = -1

class PluginInfo:
    def __init__(self, name, checksum, loader, client, message):
        self.name = name
        self.checksum = checksum
        self.loader = loader
        self.client = client
        self.message = message

class Bot(object):
    #=======================================
    # Query Information
    #=======================================
    connected = False
    spawntime = datetime.now().strftime("%A, %d. %B %Y @ %I:%M:%S%p")
    prefix = "bot." # The default command character for Autumn is "bot.".
    commands = dict()
    friends = dict()

    # =======================================
    # Watson Information
    # =======================================
    authenticator = IAMAuthenticator('YourWatsonAuthenticatorTokenHere') # This is very important. #!!!IMPORTANT!!!#
    assistant = AssistantV2(
        version='2020-04-01',
        authenticator=authenticator
    )
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/9a448ff5-627b-44b8-b4d3-22eacb7f1789')
    assistant_sessions = {}
    assistant_id = 'YourWatsonAssitantIdHere' # This is very important. #!!!IMPORTANT!!!#

    # =======================================
    # Initialization
    # =======================================
    def __init__(self):
        #=======================================
        # Bot Information
        #=======================================
        self.botNick = "Autumn" # This is very important. #!!!IMPORTANT!!!#
        self.botMaster = "Buddha#0029" # This is very important. #!!!IMPORTANT!!!#
        self.client = discord.AutoShardedClient()
        self.roles = ["autumn", "admin", "administrator", "god", "god-son", "owner", "master"]
        self.positive_reactions = ['🧐', '❤️', '👍', '🤯', '💋', '🏆', '🎃', '😎', '🌈', '🍄', '👌', '🙊', '🎂', '🥞', '😱',
                                   '🌱', '🍑', '👑', '👏', '💎', '💤', '🌼', '🍩', '🥧', '🦊', '🧁', '🎄', '🦋', '🍕', '🌸',
                                   '🍜', '💗', '💚', '🍪', '🤖', '🦕', '🌕', '🍀', '🥇']
        self.annoyed_reactions = ['😤', '😠', '😡', '🤬', '👺', '👿', '👎', '😞', '💢', '🚫', '❔', '🤯']
        #=======================================
        # Command Information
        #=======================================
        self.addDefaultCommands()
        self.addDefaultFriends()

        # =======================================
        # Settings Information
        # =======================================
        self.settings = Settings(self)

    def addDefaultFriends(self):
        self.friends["Buddha#0029"            ] = "Master" # This is very important. #!!!IMPORTANT!!!#
        self.friends["Autumn#4473"            ] = "Self" # This is very important. #!!!IMPORTANT!!!#

    def addDefaultCommands(self):
        self.commands[Bot.prefix + "god"     ] = "👽"
        self.commands[Bot.prefix + "ping"    ] = "🏓"
        self.commands[Bot.prefix + "dance"   ] = "But, I don't know how..."
        self.commands[Bot.prefix + "color"   ] = "The sky is blue, dude!"
        self.commands[Bot.prefix + "fox"     ] = "Don't worry, I don't bite..."

    def check_guild_info(self):
        guilds = {}
        if not os.path.exists(self.settings.guild_path):
            os.mkdir(self.settings.guild_path)
        guild_info_files = os.listdir(self.settings.guild_path)
        if self.client.guilds is not None:
            # Load any guild info from any files that were present.
            for guild in self.client.guilds:
                for file in guild_info_files:
                    filename = file[0:len(str(guild.id))]
                    if filename == str(guild.id) and file.find(".py"):
                        info = pickle.load(open(self.settings.guild_path + file, 'rb'))
                        guilds[str(guild.id)] = info
                        messages.printMessage("Loading guild information for: " + str(guild.id), messages.MessageType.SUCCESS)
                if not str(guild.id) in guilds.keys():
                    info = GuildInfo(str(guild.id), guild.name, self.prefix)
                    guilds[str(guild.id)] = info
                    messages.printMessage("Creating guild information for " + str(guild.id), messages.MessageType.NOTICE)
        self.settings.guild_info.update(guilds)

    def checkPlugins(self, path):
        # Obtain only Autumn plugin files.
        files = os.listdir(path)
        for file in files:
            if file.find(".py") != null:
                if file.find("discord-autumn_") == null:
                    utils.removekey(files, file)
            else:
                utils.removekey(files, file)

        # Parse them as commands.
        for i in range(len(files)):
            files[i] = self.prefix + files[i][15:-3]

        # Check the bots' list of commands against what we found.
        commands = self.commands
        plugins = dict()
        for command in commands:
            instance = commands.get(command, null)
            if instance != null:
                if isinstance(instance, str):
                    plugins[command] = instance
                else:
                    if command in files:
                        plugins[command] = instance
                    else:
                        pass # Can't edit the dict while iterating..
            else:
                pass
        self.commands = plugins

    def loadPlugins(self, path):
        self.checkPlugins(path)
        plugins = os.listdir(path)
        for plugin in plugins:
            if plugin.find(".py") != null:
                if plugin.find("discord-autumn_") != null:
                    name = plugin[15:-3] # Remove "discord-autumn_" and ".py" from the filename
                    command = self.prefix + name
                    loader = utils.Loader(self, name, null, null)
                    module = self.commands.get(command, null)
                    if module != null:
                        # Reload the module
                        try:
                            filename = Path("./plugins/discord-autumn_" + name + ".py")
                            checksum = utils.getMD5(filename)
                            if checksum != module.checksum:
                                module.checksum = checksum
                                module = import_module("plugins.discord-autumn_" + name)
                                loader.reloadPlugin(module)
                                if logging.Logger.verbosityLevel > logging.Verbosity.TRACE:
                                    messages.printMessage("Plugin reloaded - " + plugin, messages.MessageType.NOTICE)
                        except:
                            utils.removekey(self.commands, command)
                            if logging.Logger.verbosityLevel > logging.Verbosity.TRACE:
                                messages.printMessage(plugin + " has been unloaded", messages.MessageType.NOTICE)
                    else:
                        try:
                            # Make a PluginInfo and toss it into the commands dictionary.
                            checksum = utils.getMD5("./plugins/discord-autumn_" + name + ".py")
                            info = PluginInfo(name, checksum, loader, null, null)
                            self.commands[command] = info
                            if logging.Logger.verbosityLevel > logging.Verbosity.TRACE:
                                messages.printMessage("Plugin loaded - " + plugin, messages.MessageType.NOTICE)
                                messages.printMessage("Checksum: " + checksum)
                        except Exception as error:
                            messages.printMessage(plugin + " could not be loaded.", messages.MessageType.WARNING)

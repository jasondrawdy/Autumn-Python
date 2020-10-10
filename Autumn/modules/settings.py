#!/usr/bin/python
#-------------------------------------------------------------------------
# settings.py - Handles all settings for Autumn.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Serializes settings and handles the encapsulation of the bot's token.
#-------------------------------------------------------------------------

import os
import pickle
from modules import messages
from modules import logging

class Settings:

    # This is the main application key and should rarely be changed.
    api_key = "YourBotTokenHere" # This is very important. #!!!IMPORTANT!!!#

    def __init__(self, bot, version="3.0.0", path="./settings/", file="settings.autumn"):
        self.bot = bot
        self.version = version
        self.settings_path = path
        self.settings_file = file
        self.guild_info = {}
        self.guild_path = self.settings_path + "guilds/"

    def load_settings(self):
        try:
            if not os.path.exists(self.settings_path):
                os.mkdir(self.settings_path)
            if os.path.exists(self.settings_path + self.settings_file):
                if os.path.isfile(self.settings_path + self.settings_file):
                    if logging.Logger.verbosityLevel > logging.Verbosity.DEFAULT:
                        messages.printMessage("Settings have been successfully loaded!", messages.MessageType.SUCCESS)
                    else: pass
                    return pickle.load(open(self.settings_path + self.settings_file, 'rb'))
                else: messages.printMessage("The settings file exists but is corrupt.", messages.MessageType.Warning)
            else:
                messages.printMessage("No settings file exists.", messages.MessageType.EXCEPTION)
                return Settings(self.bot)
        except Exception as ex:
            messages.printMessage("I couldn't load settings.", messages.MessageType.EXCEPTION)

    def save_settings(self):
        try:
            pickle.dump(self, open(self.settings_path + self.settings_file, 'wb'))
            if logging.Logger.verbosityLevel > logging.Verbosity.DEFAULT:
                messages.printMessage("Settings have been successfully saved!", messages.MessageType.SUCCESS)
            else: pass
        except Exception as ex:
            messages.printMessage("I couldn't save settings.", messages.MessageType.EXCEPTION)

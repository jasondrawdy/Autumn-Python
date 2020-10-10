#!/usr/bin/python
#-------------------------------------------------------------------------
# guilds.py - Handles all guild information serialization for Autumn.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Handles serialization of guild information.
#-------------------------------------------------------------------------

import os
import pickle
from modules import utils
from modules import messages

null = -1

class GuildInfo(object):
    def __init__(self, id, name, prefix):
        #self.guild = guild
        self.id = id
        self.name = name
        # General settings
        self.guild_prefix = prefix
        self.custom_commands = dict()
        self.use_nlp = False
        # Moderation settings
        self.welcome_message = None
        self.server_automod = None
        self.command_cooldown = 5
        # Game settings
        self.user_profiles = None
        self.user_reminders = None
        self.rng_threshold = None

    def serialize_guild_info(self, path):
        filename = path + str(self.id) + ".agi"
        if not os.path.exists(path):
            os.mkdir(path)
        file = open(filename, 'wb')
        try:
            pickle.dump(self, file)
            messages.printMessage("Successfully saved " + self.name + "'s settings!", messages.MessageType.SUCCESS)
        except:
            messages.printMessage(self.name + "'s settings could not be saved.", messages.MessageType.EXCEPTION)

# For now we're gonna just deserialize our objects from a local directory.
# We'll populate our database when we are close to using sharding.
def get_info(path):
    # Obtain only Autumn guild information.
    files = os.listdir(path)
    for file in files:
        if not file.find(".agi") != null:
            utils.removekey(files, file)
    if len(files) > 0:
        return populate_info(files, path)
    else: return None

def populate_info(files, path):
    guilds = {}
    # Unpickle all of the guild info files.
    for file in files:
        guild = pickle.load(open(path + file, 'rb'))
        guilds[guild.id] = guild
    if len(guilds) > 0:
        return guilds
    else:
        messages.printMessage("Some guilds' info couldn't be loaded. ", messages.MessageType.WARNING)

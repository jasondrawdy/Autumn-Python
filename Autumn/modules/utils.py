#!/usr/bin/python
#-------------------------------------------------------------------------
# utils.py - Contains tools for encoding, encrypting, and others.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module contains tools for versioning, encoding, encryption and
# other utilities that may be used during the bots' server session.
#-------------------------------------------------------------------------

import os
import sys
import importlib
from importlib import import_module

from modules import logging
from modules import messages

null = -1

class Loader:
    def __init__(self, bot, plugin, message, args=[]):
        self.bot = bot
        self.plugin = plugin
        self.message = message
        self.args = args

    async def start(self):
        try:
            if logging.Logger.verbosityLevel >= logging.Verbosity.DEFAULT:
                messages.printMessage("Running '" + self.plugin + "' for %s" % str(self.message.author), messages.MessageType.NOTICE)
            await self.startPlugin(self.plugin, self.args)
        except Exception as exception:
            print(exception)
            pass

    def loadPlugin(self, name):
        module = import_module("plugins.discord-autumn_%s" % name)
        #messages.printMessage(digest, messages.MessageType.GENERAL)
        return module

    def reloadPlugin(self, module):
        #print("Refresh...")
        importlib.reload(module)
        #messages.printMessage("Plugin reloaded.", messages.MessageType.GENERAL)

    async def startPlugin(self, name, *args):
        self.plugin = self.loadPlugin(name)
        plugin = self.plugin.Plugin(self.bot, self.bot.client, self.message)
        await plugin.start(args[0])

def insert(source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

def encode(input):
    encoded = null
    version = checkVersion()
    if (version != null):
        if (checkVersion() == True): # Running Python 3.
            encoded = bytes(input, "UTF-8")
        else:
            encoded = bytes(input)
        if (encoded != null):
            return encoded
        else:
            raise Exception("The provided input could not be encoded.")
    else:
        raise Exception("The current version of Python could not be determined.")

def checkVersion():
    version = sys.version_info[0]
    if version >= 2 and version < 3:
        return False # Python 2
    elif version >= 3:
        return True # Python 3
    else:
        return False

def getMD5(filename, block=2**20):
    import hashlib
    md5 = hashlib.md5()
    try:
        file = open(filename, 'rb')
        while True:
            data = file.read(block)
            if not data:
                break
            md5.update(data)
    except IOError:
        if logging.Logger.verbosityLevel >= logging.Verbosity.DEBUG:
            messages.printMessage("File \'" + filename + "\' not found!", messages.MessageType.NONE, False)
        return None
    except:
        return None
    return md5.hexdigest()

def removekey(dictionary, key):
    index = 0
    for item in dictionary:
        if item == key:
            try:
                del dictionary[index]
                break
            except Exception as error:
                break
        index += 1

def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)

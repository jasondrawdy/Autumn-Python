#!/usr/bin/python
#-------------------------------------------------------------------------
# main.py - Minimal pre-sharded Discord bot for small to medium servers.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Autumn is a simple Discord bot meant to aid in the moderating of a single
# server under a single bot master and with minimal interaction/commands.
#-------------------------------------------------------------------------

#=======================================
## TODO:
#=======================================
"""
Add server settings for server owners
Add weather plugin
Add food plugin
Add news plugin
Add RSS plugin
Pre-shard bot
"""

#=======================================
# Imports
#=======================================
import sys
import _thread, asyncio
from bot import Bot
from modules.handler import Handler
from modules import messages
from modules import logging

#=======================================
# Variables
#=======================================

# Globals
null = -1
NONE = messages.MessageType.NONE

# Local instance of Autumn.
bot = Bot()

#=======================================
# Functions
#=======================================
def startProcessing():
    if logging.Logger.verbosityLevel >= logging.Verbosity.TRACE:
        messages.printMessage("Connecting to server...")
    try:
        # Connect to any permissible servers.
        Handler(bot).start(bot) # Create a new handler object and start it.
    except Exception as error:  # Typically when someone sends an invalid character code.
        messages.printMessage(error, messages.MessageType.EXCEPTION)
    messages.printMessage("Adiós, mi amor. 🌸", messages.MessageType.EXCEPTION)

def startResolving():
    if logging.Logger.verbosityLevel > logging.Verbosity.TRACE:
        messages.printMessage("Loading plugins...")
    sentinel = Handler(bot, "plugins")
    asyncio.run(sentinel.watch_plugins())

def startResolver():
    _thread.start_new_thread(startResolving, ())

def startBot():
    startResolver()
    if logging.Logger.verbosityLevel > logging.Verbosity.DEFAULT:
        messages.printMessage("Loading internal commands...")
        for command, obj in bot.commands.items():
            messages.printMessage(("Command: %s" % command), NONE, False)
    startProcessing()

def printGreeting():
    bold = messages.Colors.bold
    reset = messages.Colors.reset
    messages.printMessage("===================================", NONE, False)
    messages.printMessage("🌙      Welcome to: Autumn!      🌙", NONE, False)
    messages.printMessage("===================================\n", NONE, False)
    messages.printMessage("⇢ " + bold + "Author" + reset + ": Jason Drawdy (Buddha)", NONE, False)
    messages.printMessage("⇢ " + bold + "Date" + reset + ": 4.10.20", NONE, False)
    messages.printMessage("⇢ " + bold + "Version" + reset + ": 3.0.0 (Strawberry) 🍓\n", NONE, False)
    messages.printMessage("===================================", NONE, False)

#=======================================
# Initialization
#=======================================
def main():
    printGreeting()
    current = sys.path[0]
    sys.excepthook = exception_handler
    sys.path.append(current + "/modules")
    sys.path.append(current + "/plugins")
    bot.settings = bot.settings.load_settings()
    messages.printMessage("Settings Version: " + bot.settings.version)
    if logging.Logger.verbosityLevel > logging.Verbosity.DEFAULT:
        messages.printMessage("Appending system module paths...")
        for path in sys.path:
            messages.printMessage(("Path: %s" % path), NONE, False)
    startBot()
    exit(0) # End the script gracefully.

def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    messages.printMessage("Refreshing Watson session key.", messages.MessageType.INFO)

if __name__ == "__main__":
    sys.tracebacklimit = 0
    main()

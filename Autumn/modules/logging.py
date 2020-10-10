#!/usr/bin/python
#-------------------------------------------------------------------------
# logging.py - Handles all remote and local logging
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Lightweight logging class for handling both networked and local actions
#-------------------------------------------------------------------------
import os
from datetime import datetime

class Verbosity:
    NONE = 0 # No logging whatsoever.
    TRACE = 1 # Only logs entry and exit of classes and functions.
    DEFAULT = 2 # Most functions containing logs and important information.
    DEBUG = 3 # Everything that trace does except for all loops and other info.
    ALL = 4 # Literally just logs everything.

class Logger:
    verbosityLevel = Verbosity.DEFAULT
    def __init__(self, logPath):
        self.logPath = logPath
        self.logFile = self.getLogName() + ".log"
        self.logLocation = logPath + self.logFile
        pass

    def createLogEntry(self, entry):
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)
        file = open(self.logLocation, 'a')
        file.write(entry + "\n")
        file.close()

    def checkLogPath(self, path):
        if os.path.isfile(path):
            return True

    def getLogName(self):
        date = datetime.now()
        date = date.strftime("%m%d%y")
        name = "log-" + date
        return name

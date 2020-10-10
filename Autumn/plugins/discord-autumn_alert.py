#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_alert.py - Sends an alert to the bot master.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends an alert for the bot master.
#-------------------------------------------------------------------------
from datetime import datetime
import os
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        alerted = False
        message = None
        author = str(self.message.author)
        mention = str(self.message.author.mention)
        alertsPath = "plugins/alerts/"
        logPath = alertsPath + "history.log"
        time = None
        # Check if the user has recently alerted the bot master.
        if not os.path.exists(alertsPath):
            os.mkdir(alertsPath)

        if os.path.exists(logPath) and os.path.isfile(logPath):
            with open(logPath, 'rb') as f:
                lines = f.read().splitlines()
                #last_lines = self.tail(f, 25).decode('utf-8')
                count = len(lines)
                while count > 0:
                    entry = str(lines[count - 1]).split('$')
                    date = entry[0].replace("b'", "")
                    sender = entry[1].replace("'", "")
                    if sender == mention:
                        now = datetime.now().strftime("%A, %d. %B %Y @ %I:%M:%S%p")
                        format = "%A, %d. %B %Y @ %I:%M:%S%p"
                        delta = datetime.strptime(now, format) - datetime.strptime(date, format)
                        split = str(delta).split(':')
                        first = ''
                        try:
                            first = split[0].split(',')[1]
                        except:
                            first = split[0]
                        '''
                        print("Days:")
                        print(delta.days)
                        print("Hours:")
                        print(first)
                        print("Minutes:")
                        print(split[1])
                        '''
                        if delta.days < 1:
                            if int(first) < 1:
                                if int(split[1]) < 30:
                                    alerted = True
                                    time = date
                                    break
                    count -= 1

        if alerted:
            await self.message.channel.send(mention + ", you've already alerted my master on " + str(time))
        else:
            try:
                if len(args[0]) >= 2:
                    message = args[0][1:]
                if author in self.bot.friends:
                    master = False
                    smurf = False
                    for guild in self.bot.client.guilds:
                        #print(guild)
                        for member in guild.members:
                            #print(member)
                            if master is True and smurf is True:
                                break
                            if str(member) == self.bot.botMaster or str(member) == "Onyx#5550":
                                if str(member) == self.bot.botMaster:
                                    master = True
                                if str(member) == "Onyx#5550":
                                    smurf = True
                                if message is not None:
                                    await member.send("Hey! " + str(member) + " has messaged me to let you know the following:\n\n```" + message + "```")
                                    alerted = True
                                else:
                                    await member.send("Hey! " + str(member) + " has messaged me to let you know that they are looking for you!")
                                    alerted = True
                else:
                    await self.message.channel.send(mention + ", you do not have permission to use the alert feature.")
                if master is True and smurf is True and alerted is True:
                    self.log(mention, alertsPath, logPath)
                    await self.message.channel.send(mention + ", I have alerted my master for you! :heart:")
                else:
                    if alerted is False:
                        await self.message.channel.send(mention + ", unfortunately I am unable to alert my master at this time.")
                    else:
                        self.log(mention, alertsPath, logPath)
                        await self.message.channel.send(mention + ", it is `" + str(master) + "` that my master got the message on his main and `" + str(smurf) + "` on his smurf.")
            except: await self.message.channel.send(mention + ", I'm unable to send any alerts at the moment.")

    def log(self, mention, alerts_path, log_path):
        if not os.path.exists(alerts_path):
            os.mkdir(alerts_path)
        if os.path.exists(log_path):
            size = os.stat(log_path).st_size
            if size >= 500000:
                os.remove(log_path)
        now = datetime.now().strftime("%A, %d. %B %Y @ %I:%M:%S%p")
        log = now + "$" + mention + "\n"
        with open(log_path, 'a') as file:
            file.write(log)
            file.close()

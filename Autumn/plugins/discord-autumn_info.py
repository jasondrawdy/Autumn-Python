#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_info.py - Displays statistical information about Autumn.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module displays information about Autumn such as version and etc.
#-------------------------------------------------------------------------
import discord
from datetime import datetime
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        time = datetime.now().strftime("%A, %d. %B %Y @ %I:%M:%S%p")
        format = "%A, %d. %B %Y @ %I:%M:%S%p"
        delta = datetime.strptime(time, format) - datetime.strptime(self.bot.spawntime, format)
        split = str(delta).split(':')
        first = ''
        try:
            first = split[0].split(',')[1]
        except:
            first = split[0]
        uptime = str(delta.days) + " day," + first + " hours, " + split[1] + " minutes, " + split[2] + " seconds" \
            if delta.days == 1 else str(delta.days) + " days, " + first + " hours, " + split[1] + " minutes, " + split[2] + " seconds"

        info = discord.Embed(title=None, description=None, color=0xea1e63)
        info.add_field(name="Version:", value=self.bot.settings.version, inline=True)
        info.add_field(name="Library:", value="Discord.py", inline=True)
        info.add_field(name="Creator:", value="Buddha#0029", inline=True)
        info.add_field(name="Build:", value="Strawberry 🍓", inline=True)
        info.add_field(name="Discord:", value="https://discord.gg/J5UV2FB", inline=True)
        info.add_field(name="Website:", value="https://github.com/jasondrawdy/autumn-python", inline=True)
        info.set_footer(text="Cluster 1 | Shard 1 | Uptime: " + uptime)
        await self.message.channel.send(embed=info)

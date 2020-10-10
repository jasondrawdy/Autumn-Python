#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_uptime.py - Shows the time the bot has been active.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Displays the amount of time the bot has been active.
# -------------------------------------------------------------------------
import discord
import random
from datetime import datetime

class Plugin(object):
    sayings = [
        "\"Time you enjoy wasting is not wasted time.\"",
        "\"If the cracks of time were filled, where would man go?\"",
        "\"How did it get so late so soon?\"",
        "\"You can have it all. Just not all at once.\"",
        "\"Time is an illusion.\"",
        "\"Inelegantly, and without my consent, time passed.\"",
        "\"There's no advantage to hurrying through life.\"",
        "\"The lyf so short, the craft so long to lerne.\"",
        "\"Time is a storm in which we are all lost.\"",
        "\"What do ties matter, Jeeves, at a time like this?\"",
        "\"Every moment has its pleasures and its hope.\"",
        "\"There is always time for another last minute.\"",
        "\"A life is not a waste of time.\"",
        "\"Is time the wheel that turns, or the track it leaves behind?\"",
        "\"Nobody works better under pressure. They just work faster.\"",
        "\"Art is long, and Time is fleeting.\"",
    ]
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
        uptime = str(delta.days) + " **Day** " + first + " **Hours** " + split[1] + " **Minutes** " + split[2] + " **Seconds**" \
            if delta.days == 1 else str(delta.days) + " **Days** " + first + " **Hours** " + split[1] + " **Minutes** " + split[2] + " **Seconds**"

        embed = discord.Embed(title=None, description=None, color=0xea1e63)
        embed.set_thumbnail(url="https://img.icons8.com/clouds/344/hourglass.png")
        embed.add_field(name="Spawn Date:", value=self.bot.spawntime, inline=False)
        embed.add_field(name="Current Uptime:", value=uptime, inline=False)
        embed.set_footer(text=self.sayings[random.randint(0, (len(self.sayings) - 1))], icon_url="https://img.icons8.com/color/344/infinity.png")
        await self.message.channel.send(embed=embed)

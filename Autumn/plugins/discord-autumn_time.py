#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_time.py - Sends the current time to the user.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends the current time formatted in Universal Time Code.
# -------------------------------------------------------------------------
import discord
import random
from datetime import datetime, timezone

class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        time = datetime.now(timezone.utc).strftime("%I:%M %p")
        date = datetime.now(timezone.utc).strftime("%A, %d. %B %Y *(UTC)*\n`Coordinated Universal Time`")
        embed = discord.Embed(title=time, description=date, color=0xea1e63)
        await self.message.channel.send(embed=embed)

#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_test.py - Sends a test message to a channel.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends a test message to a channel.
# -------------------------------------------------------------------------
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        message = "Test module ∞ ⚭ ☨⚛︎ 🍪🍩🎂🍦🍕🍔🍟🥞🥓🥥🍓🍒🍑🍎🥝🌶🥒🥚🍏🍋🍉🍇🍅🥦🥨🍜🌮🍯🥂"
        await self.message.channel.send(message)

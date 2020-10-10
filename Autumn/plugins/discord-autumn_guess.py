#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_guess.py - Allows the user to guess a number in a range.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Allows the user to guess a number within a certain number range.
#-------------------------------------------------------------------------
import asyncio
import random

class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        min = 1
        max = 25
        answer = random.randint(min, max)
        channel = self.message.channel
        author = self.message.author.mention #str(self.message.author).split('#')[0]
        successMessage = author + ", you are correct! It is " + str(answer) + "! :cookie: "
        timeoutMessage = author + ', you took too long to answer... forget it.'
        incorrectMessage = "That was an incorrect guess. It was " + str(answer) + ".. maybe next time.. :innocent: "
        errorMessage = "I think you gave me some junk data... try an integer."
        if len(args[0]) > 2:
            await channel.send("Only one parameter is required and it should be an integer!")
        elif len(args[0]) == 2:
            try:
                guess = int(args[0][1])
                if guess > max or guess < min:
                    await channel.send("The provided number is out of the expected range (1 - 25).")
                else:
                    if guess == answer:
                        await channel.send(successMessage)
                    else:
                        await channel.send(incorrectMessage)
            except:
                await channel.send(errorMessage)
        else:
            await channel.send("OK! Send me a number within the next minute to guess the number (1 - 25).")

            def check(m):
                return m.author == self.message.author and m.channel == self.message.channel

            try:
                msg = await self.client.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await channel.send(timeoutMessage)
            else:
                try:
                    result = int(msg.content)
                    if result > max or result < min:
                        await channel.send("The provided number is out of the expected range (1 - 25).")
                    else:
                        if result == answer:
                            await channel.send(successMessage)
                        else:
                            await channel.send(incorrectMessage)
                except:
                    await channel.send(errorMessage)

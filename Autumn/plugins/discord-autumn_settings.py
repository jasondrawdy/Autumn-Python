#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_settings.py - Displays the current settings for the guild.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# Handles the configuration of guild settings.
# -------------------------------------------------------------------------
import asyncio

import discord
import random
from datetime import datetime
from modules import messages
from plugins.settings import settings_general
from plugins.settings import settings_moderation
from plugins.settings import settings_game
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        author = str(self.message.author)

        if self.message.guild is None:
            await self.message.author.send("I can't change server settings in a DM.")
        else:
            if author is self.bot.botMaster or author in self.bot.friends or self.has_permission(self.message):
                timeoutMessage = self.message.author.mention + ", I'm not worried about changing your settings anymore."
                #errorMessage = "Whoa?! I can't process your request... try an integer — :unamused:"
                #timestamp = datetime.now().strftime("%A, %d. %B %Y @ %I:%M:%S%p")
                guild_picture = ""
                if self.message.guild.icon_url is not None:
                    guild_picture = self.message.guild.icon_url
                else:pass
                profile_picture = self.message.author.avatar_url
                description = "Customize moderation tools, custom commands, and other settings for <@!693328126457151538> through this module."
                embed = discord.Embed(title="Server Settings", description=description, color=0xea1e63)
                embed.set_author(name=self.message.guild.name, url="", icon_url=guild_picture)
                embed.set_thumbnail(url="https://img.icons8.com/bubbles/344/settings.png")
                embed.add_field(name="General Settings", value="**1**. Prefix\n**2**. Custom Commands\n**3**. Bot Communication", inline=True)
                embed.add_field(name="Moderation Settings", value="**4**. Welcome\n**5**. Auto-Mod\n**6**. Cooldowns", inline=True)
                embed.add_field(name="Game Settings", value="**7**. Profiles\n**8**. Reminders\n**9**. RNG Threshold", inline=True)
                embed.set_footer(text=str(author) + " | Click on the reaction below or type exit to close this dialog.", icon_url=profile_picture)
                sent = await self.message.channel.send(embed=embed)
                await sent.add_reaction('❌')

                def check(m):
                    return m.author == self.message.author and m.channel == self.message.channel

                response = ""
                try:
                    response = await self.client.wait_for('message', check=check, timeout=60.0)
                    if response is not None:
                        if response.content.isdigit():
                            result = int(response.content)
                            if result > 9 or result < 1:
                                number = random.randint(0, len(self.bot.annoyed_reactions) - 1)
                                try: await response.add_reaction(self.bot.annoyed_reactions[number])
                                except: pass
                                await self.message.channel.send(
                                    "I didn't provide an option for '" + str(result) + "', big brain.")
                                try:
                                    await sent.delete()
                                except:
                                    pass
                            else:
                                # Process the settings choice and show the next prompt.
                                await self.process_choice(response.content)
                                #await self.message.channel.send("Unfortunately, I cannot change any settings at this time. If this is an issue, then please talk with <@530648978052874247>.")
                                try:
                                    await sent.delete()
                                    await response.delete()
                                    await self.message.delete()
                                except: pass
                        else:
                            stop_reactions = ["stop", "quit", "leave", "exit", "no", "nvm", "nevermind", "forget it", "idk"]
                            if response.content in stop_reactions:
                                try:
                                    await sent.delete()
                                    await response.delete()
                                    await self.message.delete()
                                except: pass
                            else:
                                try:
                                    await sent.delete()
                                    number = random.randint(0, len(self.bot.annoyed_reactions) - 1)
                                    try: await response.add_reaction(self.bot.annoyed_reactions[number])
                                    except: pass
                                    await self.message.channel.send(
                                        "I didn't provide an option for '" + str(response.content) + "', big brain.")
                                    await response.delete()
                                    await self.message.delete()
                                except:
                                    pass
                    else:
                        await self.message.channel.send("Yeah... you're response should not be null.")
                        try:
                            number = random.randint(0, len(self.bot.annoyed_reactions) - 1)
                            try: await response.add_reaction(self.bot.annoyed_reactions[number])
                            except:pass
                            # await self.message.channel.send(errorMessage)
                            await sent.delete()
                            await response.delete()
                            await self.message.delete()
                        except:
                            pass
                except asyncio.TimeoutError:
                    await self.message.channel.send(timeoutMessage)
                    await sent.delete()
                    await self.message.delete()
            else:
                await self.message.channel.send("Only my master or a server administrator can change my settings.")

    def has_permission(self, message):
        roles = []
        for member in message.guild.members:
            if member.id == message.author.id:
                roles = member.roles
                break
            else: pass
        if len(roles) > 0:
            for role in roles:
                if role.permissions.administrator:
                    return True
                else:
                    split = role.name.split(' ')
                    if split[0].lower() in self.bot.roles:
                        return True
                    else: pass
            return False
        else: return False

    async def process_choice(self, choice):
        prompts = {
            '1': settings_general.change_prefix,
            '2': None,
            '3': settings_general.change_nlp,
            '4': None,
            '5': None,
            '6': None,
            '7': None,
            '8': None,
            '9': None
        }
        instance = prompts.get(str(choice))
        if instance is None:
            await self.message.channel.send("I'm unable to configure those settings right now.")
        else:
            result = await instance(self.bot, self.message)
            if result:
                if result == "timeout":
                    pass
                else:
                    await self.message.channel.send("Your settings have been saved.")  # prompts.get(choice)
            else:
                if result == "timeout":
                    pass
        '''
        if int(choice) == 1:
            result = await settings_general.change_prefix(self.bot, self.message)
            if result:
                if result == "timeout": pass
                else:
                    await self.message.channel.send("Your settings have been saved.")  # prompts.get(choice)
            else:
                if result == "timeout": pass
                else:
                    await self.message.channel.send("I can't change settings at the moment.")
        else:
            await self.message.channel.send("I'm unable to configure those settings right now.")
        '''

#!/usr/bin/python
# -------------------------------------------------------------------------
# settings_general.py - Handles all things related to settings for Autumn.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module handles guild settings such as prefixes for Autumn.
# -------------------------------------------------------------------------
import discord
import asyncio
import random


async def change_prefix(bot, message):
    sent = await message.channel.send("Please enter the prefix for my commands. Examples: '!', '@', '$', or even words and symbols like - 'bot.'")

    def check(m):
        return m.author == message.author and m.channel == message.channel

    response = ""
    confirm = ""
    try:
        response = await bot.client.wait_for('message', check=check, timeout=60.0)
        if response is not None:
            trimmed = "".join(response.content.split())
            confirm = await message.channel.send("Are you sure you want to change the prefix to: '" + trimmed + "'?")
            check = await bot.client.wait_for('message', check=check, timeout=60.0)
            if check is not None:
                content = "".join(check.content.split())
                if content == "yes" or content == "y":
                    count = len(bot.settings.guild_info)
                    if count is not None:
                        for guild in bot.settings.guild_info:
                            if guild == str(message.author.guild.id):
                                info = bot.settings.guild_info[guild]
                                info.guild_prefix = trimmed
                                entry = {guild: info}
                                bot.settings.guild_info.update(entry)
                                bot.settings.guild_info[guild].serialize_guild_info(bot.settings.guild_path)
                                print(str(
                                    message.author.mention) + " has modified settings for " + message.author.guild.name)
                                return True
                            else:
                                pass
                        return False
                    else:
                        return False
                else:
                    if content == "no" or content == "n":
                        await change_prefix(bot, message)
                    else:
                        try:
                            await sent.delete()
                            await response.delete()
                            await confirm.delete()
                            await message.delete()
                        except: pass
            else:
                await change_prefix(bot, message)
        else:
            await message.channel.send("Yeah... you're response should not be null.")
            try:
                await sent.delete()
                await response.delete()
                await message.delete()
            except: pass
    except asyncio.TimeoutError:
        await message.channel.send(message.author.mention + ", don't worry about it... I closed the settings menu.")
        try:
            await sent.delete()
            await confirm.delete()
            await message.delete()
        except: pass
        return "timeout"


async def change_nlp(bot, message):
    title = "Natural Language Processing"
    description = "This module allows an administrator to enable Autumn's ability to process natural messages for a context she can understand."
    state = None
    x = False
    if bot.settings.guild_info is not None:
        for guild in bot.settings.guild_info:
            if guild == str(message.author.guild.id):
                enabled = bot.settings.guild_info[guild].use_nlp
                if enabled:
                    x = True
                    state = "N.L.P is currently `Enabled`! Type ***disable*** to deactive the module."
                else:
                    state = "N.L.P is currently `Disabled`. Type ***enable*** to activate the module!"
    embed = discord.Embed(title=title, description=description)
    embed.add_field(name="Current Status:", value=state, inline=False)
    sent = await message.channel.send(embed=embed)

    def check(m):
        return m.author == message.author and m.channel == message.channel

    response = ""
    try:
        response = await bot.client.wait_for('message', check=check, timeout=60.0)
        if response is not None:
            try:
                trimmed = "".join(response.content.split())
                if trimmed == "enable":
                    if x:
                        await message.channel.send("N.L.P is already enabled you dork!")
                        raise Exception
                    else:
                        for guild in bot.settings.guild_info:
                            if guild == str(message.author.guild.id):
                                info = bot.settings.guild_info[guild]
                                info.use_nlp = True
                                entry = {guild: info}
                                bot.settings.guild_info.update(entry)
                                bot.settings.guild_info[guild].serialize_guild_info(bot.settings.guild_path)
                                print(str(message.author.mention) + " has modified settings for " + message.author.guild.name)
                                try:
                                    await sent.delete()
                                    await response.delete()
                                    await message.delete()
                                except: pass
                                return True
                            else:
                                pass
                elif trimmed == "disable":
                    if not x:
                        await message.channel.send("N.L.P is already disabled, big brain...")
                        raise Exception
                    else:
                        for guild in bot.settings.guild_info:
                            if guild == str(message.author.guild.id):
                                info = bot.settings.guild_info[guild]
                                info.use_nlp = False
                                entry = {guild: info}
                                bot.settings.guild_info.update(entry)
                                bot.settings.guild_info[guild].serialize_guild_info(bot.settings.guild_path)
                                print(str(
                                    message.author.mention) + " has modified settings for " + message.author.guild.name)
                                try:
                                    await sent.delete()
                                    await response.delete()
                                    await message.delete()
                                except: pass
                                return True
                            else:
                                pass
                else:
                    raise Exception
            except:
                await sent.delete()
                await response.delete()
                await message.delete()
                return "timeout"
        else:
            await message.channel.send("Yeah... you're response should not be null.")
            try:
                await sent.delete()
                await response.delete()
                await message.delete()
            except: pass
            return False
    except asyncio.TimeoutError:
        await message.channel.send(message.author.mention + ", don't worry about it... I closed the settings menu.")
        try:
            await sent.delete()
            await response.delete()
            await message.delete()
        except: pass
        return "timeout"

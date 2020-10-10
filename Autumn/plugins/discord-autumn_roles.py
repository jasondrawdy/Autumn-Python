#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_roles.py - Sends a friendly hello to the sender.
# Author: Jason Drawdy (Buddha)
# Date: 4.12.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module handles roles within a given server.
# -------------------------------------------------------------------------
import asyncio
from modules import messages

class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        error = self.message.author.mention + ", I don't understand what that means..."
        if len(args[0]) >= 2:
            options = {
                "get": self.getRole(),
                "set": self.setRole(),
                "remind": self.remind()
            }
            option = args[0][1]
            process = options.get(option, self.respond(error))
            await process
        else:
            await self.message.channel.send("What would you like to do with roles?")
    async def respond(self, message):
        await self.message.channel.send(message)
    async def remind(self):
        try:
            if str(self.message.author) in self.bot.friends:
                reminded = 0
                guild = self.message.author.guild
                reminder = "**NOTICE**: This is a reminder to please obtain a role within *" + str(guild.name) + "* by using the roles command by " \
                           "typing — *bot.roles get* — in order for me to stop nagging you about it. And, you know that I wouldn't do it if I didn't love you. :heart:\n\n" \
                           "If you need help understanding commands or how I operate then type: *autumn.help* for more information. :kiss:"
                for member in guild.members:
                    if member.top_role is guild.default_role:
                        try:
                            await member.send(reminder)
                            messages.printMessage(str(member.name) + " has been reminded!")
                            reminded += 1
                        except:
                            messages.printMessage(member.name + " was unable to be reminded.")
                    else:
                        pass
                if reminded > 0:
                    await self.message.channel.send("Users have been reminded about their roles!")
                else:
                    await self.message.channel.send("Not all users could be reminded about their roles.")
            else:
                await self.message.channel.send("Only my master or a server administrator can remind users about roles.")
        except:
            await self.message.channel.send("I'm unable to remind users about their roles...")

    async def getRole(self):
        try:
            for member in self.message.author.guild.members:
                if str(member.id) == str(self.message.author.id):
                    author = str(self.message.author)
                    mods = {
                        "グラヴィディオン#6541": self.setAdmin(member),
                        "Gummo#1905": self.setAdmin(member),
                        "haezz#8045": self.setMod(member)
                    }
                    if author in mods:
                        await mods[author]
                        break
                    else:
                        await self.setStandard(member)
                        break
                    break
                else:pass
        except Exception as ex:
            await self.message.channel.send("I'm unable to change any roles.")

    async def setRole(self):
        if self.message.author == self.bot.botMaster or self.message.author.top_role.permissions.administrator:
            await self.message.channel.send("Setting a new role...")
        else:pass

    async def setMod(self, member):
        try:
            roles = member.guild.roles
            default = str(member.guild.default_role).lower()
            highest = str(member.top_role).lower()
            if highest == 'admin' or highest == 'administrator' or "owner" in highest or "notorious" in highest or "mod" in highest or "moderator" in highest:
                await self.message.channel.send(self.message.author.mention + ", you are already an moderator!")
            else:
                if highest == default:
                    for role in roles:
                        name = str(role.name).lower()
                        if not "mod" in name or "moderator" in name:
                            pass
                        else:
                            await member.add_roles(role)
                            await self.message.channel.send(self.message.author.mention + ", your roles have been updated!")
                            break
                else:pass
        except Exception as ex:
            await self.message.channel.send("I'm unable to change your role.")

    async def setAdmin(self, member):
        try:
            roles = member.guild.roles
            default = str(member.guild.default_role).lower()
            highest = str(member.top_role).lower()
            if highest == 'admin' or highest == 'administrator' or "owner" in highest or "notorious" in highest:
                await self.message.channel.send(self.message.author.mention + ", you are already an administrator!")
            else:
                if highest == default:
                    for role in roles:
                        name = str(role.name).lower()
                        if not "admin" in name or "administrator" in name or "owner" in name or "notorious" in name:
                            pass
                        else:
                            await member.add_roles(role)
                            await self.message.channel.send(self.message.author.mention + ", your roles have been updated!")
                            break
                else:pass
        except Exception as ex:
            await self.message.channel.send("I'm unable to change your role.")

    async def setStandard(self, member):
        try:
            roles = member.guild.roles
            default = str(member.guild.default_role).lower()
            highest = str(member.top_role).lower()
            if highest == default:
                count = 1
                while (True):
                    if count < len(roles):
                        try:
                            role = str(roles[count].name).lower()
                            if "bot" not in role and "dyno" not in role and "rythm" not in role:
                                permissions = roles[count].permissions
                                if not permissions.administrator and not permissions.manage_guild and not permissions.manage_channels:
                                    await member.add_roles(roles[count])
                                    await self.message.channel.send(self.message.author.mention + ", your roles have been updated!")
                                    break
                                else:
                                    count += 1
                            else:
                                count += 1
                                pass
                        except:
                            count += 1
                    else:
                        raise Exception("There are no roles to be added.")
            else:
                await self.message.channel.send(self.message.author.mention + ", you already have a role!")
        except Exception as ex:
            await self.message.channel.send("I'm unable to change your role.")

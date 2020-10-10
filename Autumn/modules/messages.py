#!/usr/bin/python
# -------------------------------------------------------------------------
# messages.py - Processes all incoming messages from the IRC server.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module processes all messages received from the Discord server and
# directs input and output to the proper functions/modules.
# -------------------------------------------------------------------------
import discord
import json
from datetime import datetime
from modules import commands
from modules import utils
from modules import logging
from ibm_watson import ApiException

null = -1

class MessageType:
    NONE = 0
    GENERAL = 1
    NOTICE = 2
    SUCCESS = 3
    WARNING = 4
    EXCEPTION = 5

class MessageInfo:
    def __init__(self, message, sender, channel):
        self.message = message
        self.sender = sender
        self.channel = channel

class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class Foreground:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Background:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

def printMessage(message, type=MessageType.GENERAL, timestamps=True, log=True):
    try:
        data = message
        switch = {
            MessageType.NONE: "" + Colors.reset,
            MessageType.GENERAL: "[" + Colors.Foreground.lightgrey + "-" + Colors.reset + "]: ",
            MessageType.NOTICE: "[" + Colors.Foreground.orange + "i" + Colors.reset + "]: ",
            MessageType.SUCCESS: "[" + Colors.Foreground.green + "+" + Colors.reset + "]: ",
            MessageType.WARNING: "[" + Colors.Foreground.yellow + "!" + Colors.reset + "]: ",
            MessageType.EXCEPTION: "[" + Colors.Foreground.red + "x" + Colors.reset + "]: "
        }
        accent = switch.get(type, "")
        if timestamps:
            date = datetime.now()
            timestamp = date.strftime("%A, %d. %B %Y @ %I:%M:%S%p")
            message = "(" + Colors.Foreground.lightgrey + timestamp + Colors.reset + ") " + accent + data
        else:
            message = accent + data
    except:pass

    if log:
        logging.Logger("./log/").createLogEntry(message)

    message = addColor(message)
    print(message)

def addColor(message):
    # Text is colorized at different spots.
    x = message
    y = x
    if x.find("Autumn"):
        color = Colors.Foreground.pink + "Autumn" + Colors.reset
        y = y.replace("Autumn", color)
    if x.find("Buddha"):
        color = Colors.Foreground.purple + "Buddha" + Colors.reset
        y = y.replace("Buddha", color)
    return y

async def processMessage(bot, message):
    # Log what the server sent us.
    data = message.content.strip()
    if data:
        printMessage(str(message.author) + ": " + data, MessageType.SUCCESS, True)
        bundle = commands.isCommand(bot, message)
        #print(bundle.message.content)
        if message.author == bot.client.user:
            return
        if message.content == "bot.help":
            await commands.processCommand(bundle)
            return
        if bundle is not None:
            await commands.processCommand(bundle)
        else:
            if bot.settings.guild_info is not None:
                try:
                    for guild in bot.settings.guild_info:
                        if guild == str(message.author.guild.id):
                            if bot.settings.guild_info[str(message.author.guild.id)].use_nlp:
                                await process_with_watson(bot, message)
                except:
                    await process_with_watson(bot, message)

async def process_with_watson(bot, message):
    try:
        # Try to process the message through Watson for a response.
        if len(bot.assistant_sessions) > 0 and str(
                message.author.mention) in bot.assistant_sessions.keys():
            try:
                # Use the current session to communicate with Watson.
                # print("Using the current session with Watson.")
                await process_response(bot, message)
            except ApiException:
                # Create an instance of the Watson assistant.
                # print("Creating a new session with Watson; the other has expired.")
                await create_watson_session(bot, message)
        else:
            # Create a new session with Watson.
            # print("Creating a new session with Watson.")
            await create_watson_session(bot, message)
    except: pass

async def create_watson_session(bot, message):
    try:
        await delete_watson_session(bot, message)
        user = str(message.author.mention)
        response = bot.assistant.create_session(
            assistant_id=bot.assistant_id
        ).get_result()
        session = json.dumps(response, indent=2)
        id = json.loads(session)['session_id']
        bot.assistant_sessions[user] = id
        # await process_response(bot, message)
        #print(id)
        if id is not None:
            await process_response(bot, message)
        else:
            pass
    except ApiException: pass
    except Exception as ex:
        #print(ex)
        pass

async def delete_watson_session(bot, message):
    try:
        response = bot.assistant.delete_session(
            assistant_id=bot.assistant_id,
            session_id=bot.assistant_sessions[str(message.author.mention)]
        ).get_result()
    except ApiException: pass
    except:
        pass

async def process_response(bot, message):
    response = bot.assistant.message(
        assistant_id=bot.assistant_id,
        session_id=bot.assistant_sessions[str(message.author.mention)],
        input={
            'message_type': 'text',
            'text': message.content,  # 'Hello'
            'options': {
                'return_context': True
            }
        },
    ).get_result()
    # Process any recipes
    result = json.dumps(response, indent=2)
    #print(result)
    await handle_message(bot, result, message)

async def handle_message(bot, result, message):

    #await check_user_permissions(bot, result, message)

    context = {}
    response = None
    intent = None
    #print(result)
    try:
        intent = json.loads(result)['output']['intents'][0]['intent']
    except: pass
    if intent is not None and 'dialog_exit' == intent:
        #print(intent)
        await delete_watson_session(bot, message)
    else:
        stop_reactions = ["stop", "quit", "leave", "exit", "no", "nvm", "nevermind", "forget it", "idk"]
        try:
            context = json.loads(result)['context']['skills']['main skill']['user_defined']
        except:
            context = json.loads(result)['context']['skills']['main skill']
        #print('CONTEXT')
        #print(context)

        for_bot = False
        output = json.loads(result)['output']
        entities = output['entities']
        #print(entities)
        if len(entities) > 0:
            if entities[0]['entity'] == 'Autumn':
                #print(True)
                for_bot = True

        if 'get_message' in context.keys() and context['get_message']:
            # DM the user since we have their handle and a message.
            if 'should_dm' in context.keys() and context['should_dm']:
                message.content = "bot.dm " + context['username'] + " " + context['message']
                bundle = commands.CommandBundle(bot, message, bot.prefix)
                await commands.processCommand(bundle)
                await delete_watson_session(bot, message)
        elif 'get_user' in context.keys() and context['get_user']:
            if str(message.content).lower() in stop_reactions:
                await delete_watson_session(bot, message)
            else:
                # Check that user is valid.
                if isLegitUser(context['username']):
                    context['user_valid'] = True
                    if 'should_kick' in context.keys() and context['should_kick']:
                        # Try to kick the user.
                        message.content = "bot.kick " + context['username']
                        bundle = commands.CommandBundle(bot, message, bot.prefix)
                        await commands.processCommand(bundle)
                        await delete_watson_session(bot, message)
                    elif 'should_ban' in context.keys() and context['should_ban']:
                        # Try to ban the user.
                        message.content = "bot.ban " + context['username']
                        bundle = commands.CommandBundle(bot, message, bot.prefix)
                        await commands.processCommand(bundle)
                        await delete_watson_session(bot, message)
                    else:
                        # We're gonna provide a message with the username.
                        response = output['generic'][0]['text']
                else:
                    context['user_valid'] = False
                    response = "That isn't a valid user. Try again with a mentionable user."
                    await delete_watson_session(bot, message)
        elif 'send_alert' in context.keys() and context['send_alert']:
            message.content = "bot.alert"
            bundle = commands.CommandBundle(bot, message, bot.prefix)
            await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
            await delete_watson_session(bot, message)
        elif 'update_status' in context.keys() and context['update_status']:
            # Update Autumn's status with the input provided by the user.
            if context['bot_status'].lower() in stop_reactions:
                await delete_watson_session(bot, message)
            else:
                message.content = "bot.status " + context['bot_status']
                bundle = commands.CommandBundle(bot, message, bot.prefix)
                await commands.processCommand(bundle)
                await delete_watson_session(bot, message)
        elif 'show_quote' in context.keys() and context['show_quote']:
            # Calculate a formula provided by the user.
            message.content = "bot.quote"
            bundle = commands.CommandBundle(bot, message, bot.prefix)
            await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
        elif 'get_guess' in context.keys() and context['get_guess']:
            # Calculate a formula provided by the user.
            message.content = "bot.guess " + context['number']
            bundle = commands.CommandBundle(bot, message, bot.prefix)
            await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
        elif 'get_equation' in context.keys() and context['get_equation']:
            # Calculate a formula provided by the user.
            message.content = "bot.math " + context['math_equation']
            bundle = commands.CommandBundle(bot, message, bot.prefix)
            await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
        elif 'show_info' in context.keys() and context['show_info']:
            # Show help information for Autumn.
            message.content = "bot.info"
            bundle = commands.CommandBundle(bot, message, bot.prefix)
            await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
        elif 'show_current_time' in context.keys() and context['show_current_time']:
            # Show time related information about Autumn.
            message.content = "bot.time"
            bundle = commands.CommandBundle(bot, message, bot.prefix)
            await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
        elif 'show_uptime' in context.keys() and context['show_uptime']:
            # Show time related information about Autumn.
            message.content = "bot.uptime"
            bundle = commands.CommandBundle(bot, message, bot.prefix)
            await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
        elif 'show_help' in context.keys() and context['show_help']:
            # Show time related information about Autumn.
            content = message.content
            if not '.help' in content and not '!help' in content and not '@help' in content:
                message.content = "bot.help"
                bundle = commands.CommandBundle(bot, message, bot.prefix)
                await commands.processCommand(bundle)
            await delete_watson_session(bot, message)
        else:
            try:
                response = output['generic'][0]['text']
                edited = response.replace("{user}", str(message.author.mention))
                if response.find('{user}'):
                    response = edited
                else:
                    pass
            except ApiException:
                pass
            except:
                pass
        if response is not None:
            #print(intent)
            if intent is not None:
                if 'response_insults' == intent and not for_bot:
                    pass
                elif 'response_greeting' == intent and not for_bot:
                    pass
                else:
                    if await check_user_permissions(bot, result, message):
                        await message.channel.send(response)

async def check_user_permissions(bot, result, message):
    can_kick = False
    can_ban = False
    try:
        roles = message.author.roles
        for role in roles:
            if role.permissions.administrator or role.permissions.ban_members:
                can_ban = True
                break
            elif role.permissions.kick_members:
                can_kick = True
                break
    except: pass

    try:
        intent = json.loads(result)['output']['intents'][0]['intent']
        #print(intent)
        #print("Kick: " + str(can_kick))
        #print("Ban: " + str(can_ban))
        if 'plugin_alert' == intent:
            if not str(message.author) in bot.friends:
                response = message.author.mention + ", you're not one of my friends... so, umm.. I'm not gonna do that for you."
                await message.channel.send(response)
                return False
        if 'plugin_dm' == intent:
            if not can_ban and str(message.author) != bot.botMaster:
                await message.channel.send("You don't have permission to private message anybody.")
                return False
        if 'plugin_kick' == intent:
            if not can_kick and not can_ban:
                await message.channel.send("You don't have permission to kick anybody.")
                return False
        if 'plugin_ban' == intent:
            if not can_ban:
                await message.channel.send("You don't have permission to ban anybody.")
                return False
        if 'plugin_status' == intent:
            if str(message.author) != bot.botMaster:
                await message.channel.send("You don't have permission to change my status.")
                return False
        return True
    except ApiException: pass
    except: pass

def isLegitUser(user):
    if "<@!" in user:
        return True
    else:
        return False

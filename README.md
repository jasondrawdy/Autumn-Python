![Banner](https://user-images.githubusercontent.com/40871836/95787882-5e3c9600-0ca8-11eb-95e7-9e5a91bf1e4f.jpg)
# Autumn-Python
Autumn is a simple and extensible Discord bot aimed at helping with moderation and user-friendliness. The goal of the bot is to be as accessible, user-friendly, and extensible as possible which is accentuated by asynchronous initialization, multi-threading, and of course dynamic plugin loading. With these features in place it is possible to create an entirely new Discord bot because of the plug-and-play nature of the code.

# Note
**Important**: All previous functionality is being replaced with the new 1.5+ update of Discord.py.

# Features
- Asynchronous
- Multithreaded
- Event based
- Dynamic plugin loading
- Colorized log output

# Requirements
- **Python 3**  
`brew install python` or `sudo apt install python3-pip`
- **Discord.Py**:  
`pip3 install discord.py`  
- **IBM Watson SDK**:  
`pip3 install ibm_watson`  

# Getting Started
When running Autumn for the first time, it will try and automatically connect to the Discord service with the current bot token, however, the token of the bot must be changed. The bot's token or `api_key` can be found in the file `./modules/settings.py`. Next, if it is desired to utilize the NLP or Natural Language Processing functionality of the bot, an authentication token and a Watson assistant id must be created; and all of the relevant information can be found here: https://cloud.ibm.com/docs/assistant?topic=assistant-getting-started.

The bot's authentication token and Watson assitant id variables can be found in `./bot.py`.

****Note:**** *Autumn utilizes parts of the Discord.Py library, however, it has been written to be mostly proprietary in terms of commands.*

# Plugins
Currently there are only a handful of plugins (commands) for the bot because of simplicity and keeping the codebase fairly small. Most plugins that aren't available can be created from the provided plugin templates. Along with dynamically loaded plugins, the bot also features internal commands which can be modified from within the `bot.py` file. The commands that already exist are again, very simple such as replying to the bot's name, replying with the sky's color, or even just a friendly hello.

### Current Plugins:
**Note**: Admin commands can only be run by the bot master and nobody else.

| Plugin            | Private   | Description                        |
|-------------------|:---------:|------------------------------------|
| autumn_hi.py      | No        | Sends hello to the sender          |
| autumn_kick.py    | Yes       | Kicks a user from the server       |
| autumn_ban.py     | Yes       | Bans a user from server            |
| autumn_ping.py    | No        | Sends a ping reply to the user     |
| autumn_test.py    | No        | Sends a test message to the sender |

And of course there are a lot more packaged with the bot and more that can be developed!

### Plugin Template:
~~If you would like to create a plugin for Autumn you can do so by following the structure of the template below. The template is actually fairly straight-forward and easy to follow. The first thing to notice is that the `bot` object, `sender`, and the `channel` if any, are provided to the plugin upon startup. The plugin is also provided any given args and the first real argument can typically be accessed at `args[0][0]`. Also, another point to take notice of is since the plugins are dynamically loaded any changes that are saved will be reflected in a nearly real-time state. The final and most important aspect of plugins for the bot is the naming convention. Right now, plugin files need to have the prefix of `discord-autumn_` and then the actual plugin name such as *`hi`* for example; and thus making the full name of the file itself `discord-autumn_hi.py` and therefore recognizable by the bot for loading into its dictionary.~~

#### Greetings Plugin
```python
#!/usr/bin/python
#-------------------------------------------------------------------------
# discord-autumn_hi.py - Sends a friendly hello to the sender.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module sends a hello to a user who originally greeted Autumn.
#-------------------------------------------------------------------------
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        message = "Hi, " + self.message.author.mention + "! :heart:"
        await self.message.channel.send(message)

```

#### Status Plugin
```python
#!/usr/bin/python
# -------------------------------------------------------------------------
# discord-autumn_status.py - Changes the current status of the bot.
# Author: Jason Drawdy (Buddha)
# Date: 4.10.20
# Version: 3.0.0 (Strawberry)
#
# Description:
# This module handles the configuration of the bot's current status.
# -------------------------------------------------------------------------
import discord
class Plugin(object):
    def __init__(self, bot, client, message):
        self.bot = bot
        self.client = client
        self.message = message

    async def start(self, *args):
        if str(self.message.author) == self.bot.botMaster:
            if len(args[0]) < 1:
                await self.message.channel.send("Enter a status for me to use!")
            else:
                message = ' '.join(args[0][1:])
                status = discord.Activity(type=discord.ActivityType.watching, name=message)
                await self.client.change_presence(activity=status)
                await self.message.channel.send(self.message.author.mention + ", my status has been updated!")
        else:
            await self.message.channel.send("Only my master can change my status, silly.")

```
# License
Copyright © ∞ Jason Drawdy

All rights reserved.

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the above copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization.

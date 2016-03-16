import discord

import buttcore
from buttcore import client, handler
from buttcore.util import load_commands

@handler("reload")
async def reload(data):
    await load_commands(buttcore.commands)

@handler("say")
async def say(data):
    if "channel" not in data or "text" not in data:
        return

    channel = client.get_channel(str(data["channel"]))

    if channel:
        await client.send_message(channel, data["text"])

@handler("game")
async def game(data):
    if "game" not in data:
        return

    await client.change_status(discord.Game(data["game"]))

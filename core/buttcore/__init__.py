import discord
import asyncio
import os
import re
import json
import logging

from buttcore.database import get_redis

logging.basicConfig(level=logging.INFO)

COMMAND_PREFIX = r"!"

if "example.com" in os.environ["DISCORD_USERNAME"]:
    raise ValueError("Please set your DISCORD_USERNAME to a valid username.")

client = discord.Client()
commands = {}

async def load_commands():
    global commands

    redis_client = await get_redis()
    commands = await redis_client.hgetall_asdict("bot:commands")

    print("Loaded %s commands." % (len(commands)))
    redis_client.close()

async def on_pubsub(ps_message):
    print(ps_message)

    try:
        data = json.loads(ps_message.value)
    except ValueError:
        print("ValueError trying to parse '%s'" % (ps_message.value))
        return

    if "action" not in data:
        return

    if data["action"] == "reload":
        await load_commands()
    elif data["action"] == "say":
        if "channel" not in data or "text" not in data:
            return

        channel = client.get_channel(str(data["channel"]))

        if channel:
            await client.send_message(channel, data["text"])
    elif data["action"] == "game":
        if "game" not in data:
            return

        await client.change_status(discord.Game(data["game"]))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await load_commands()

    redis_client = await get_redis()
    subscriber = await redis_client.start_subscribe()
    await subscriber.psubscribe(["core:*"])

    while True:
        reply = await subscriber.next_published()
        await on_pubsub(reply)

    # When finished, close the connection.
    redis_client.close()

@client.event
async def on_message(message):
    redis_client = await get_redis()

    if message.content.startswith(COMMAND_PREFIX + "help"):
        output = ""

        for command, meta in commands.items():
            output += "**{command}** - {help}\n".format(
                command=command,
                help=meta
            )

        if output.strip() == "":
            await client.send_message(message.channel, "No external commands have been loaded.")
        else:
            await client.send_message(message.channel, output.strip())
    elif message.content.startswith(COMMAND_PREFIX + "ping"):
        await client.send_message(message.channel, 'Core is alive.')
    else:
        for command in commands:
            if re.search(r"^" + COMMAND_PREFIX + command, message.content, re.I):
                await redis_client.publish("command:" + command, json.dumps({
                    "message": {
                        "id": message.id,
                        "content": message.content
                    },
                    "channel": message.channel.id,
                    "author": {
                        "id": message.author.id,
                        "name": message.author.name,
                        "discriminator": message.author.discriminator
                    }
                }))

    redis_client.close()

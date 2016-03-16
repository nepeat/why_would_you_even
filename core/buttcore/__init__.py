import discord
import asyncio
import os
import json
import logging

from buttcore.database import get_redis
from buttcore.util import load_commands, jsonify_message

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

COMMAND_PREFIX = r"!"

if "example.com" in os.environ["DISCORD_USERNAME"]:
    raise ValueError("Please set your DISCORD_USERNAME to a valid username.")

client = discord.Client()
commands = {}
core_handlers = {}

def handler(action, **kwargs):
    def decorator(f):
        core_handlers[action] = f
        return f
    return decorator

async def on_pubsub(ps_message):
    log.info(ps_message)

    try:
        data = json.loads(ps_message.value)
        action = ps_message.channel.split(":", 2)[1]
    except ValueError:
        log.error("ValueError trying to parse '%s'" % (ps_message.value))
        return

    for handler, callback in core_handlers.items():
        if action == handler:
            await callback(data)

@client.event
async def on_ready():
    log.info('Logged in as')
    log.info(client.user.name)
    log.info(client.user.id)
    log.info('------')
    await load_commands(commands)

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
            if message.content.strip().lower().startswith(COMMAND_PREFIX + command):
                await redis_client.publish("command:" + command, jsonify_message(message))

    redis_client.close()

# Import handlers last
import buttcore.handlers

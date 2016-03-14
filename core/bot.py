import discord
import asyncio
import os
import sys
import re
import asyncio_redis
import json

COMMAND_PREFIX = r"!"

client = discord.Client()
commands = {}

async def get_redis():
    return await asyncio_redis.Connection.create(
        host=os.environ.get("REDIS_HOST", "127.0.0.1"),
        port=os.environ.get("REDIS_PORT", 6379),
        db=os.environ.get("REDIS_DB", 0),
        encoder=asyncio_redis.encoders.UTF8Encoder()
    )

async def load_commands():
    redis_client = await get_redis()
    try:
        commands.clear()
        rawcommands = await redis_client.get("bot:commands")
        commands.update(json.loads(rawcommands))
    except (TypeError, ValueError):
        pass

    print("Loaded %s commands." % (len(commands)))

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
    connection.close()

@client.event
async def on_message(message):
    redis_client = await get_redis()

    if message.content.startswith(COMMAND_PREFIX + "help"):
        output = ""

        for command, meta in commands.items():
            output += "**{command}** {help}\n".format(
                command=command,
                help=meta["help"]
            )

        if output.strip() == "":
            await client.send_message(message.channel, "No external commands have been loaded.")
        else:
            await client.send_message(message.channel, output.strip())
    elif message.content.startswith(COMMAND_PREFIX + "ping"):
        await client.send_message(message.channel, 'Core is alive.')
    else:
        for command, meta in commands.items():
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

if "example.com" in os.environ["DISCORD_USERNAME"]:
    raise ValueError("Please set your DISCORD_USERNAME to a valid username.")

if __name__ == "__main__":
    print("Bot started!")

    client.run(
        os.environ["DISCORD_USERNAME"],
        os.environ["DISCORD_PASSWORD"]
    )

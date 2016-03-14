import discord
import asyncio
import os
import re
import redis

redis_client = redis.StrictRedis(
    host=os.environ.get("REDIS_HOST", "127.0.0.1"),
    port=os.environ.get("REDIS_PORT", 6379),
    db=os.environ.get("REDIS_DB", 0)
)

client = discord.Client()

commands = {}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    load_commands()

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
if "example.com" in os.environ["DISCORD_USERNAME"]:
    raise ValueError("Please set your DISCORD_USERNAME to a valid username.")

client.run(
    os.environ["DISCORD_USERNAME"],
    os.environ["DISCORD_PASSWORD"]
)

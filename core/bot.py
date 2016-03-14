import discord
import asyncio
import os
import re
import redis
import json
import signal

redis_client = redis.StrictRedis(
    host=os.environ.get("REDIS_HOST", "127.0.0.1"),
    port=os.environ.get("REDIS_PORT", 6379),
    db=os.environ.get("REDIS_DB", 0)
)

client = discord.Client()

commands = {}

def load_commands(ps_message=None):
    try:
        commands.update(json.loads(redis_client.get("bot:commands")))
    except (TypeError, ValueError):
        pass

def on_pubsub(ps_message):
    print(ps_message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    load_commands()

@client.event
async def on_message(message):
    if message.content.startswith('!help'):
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
    elif message.content.startswith('!ping'):
        await client.send_message(message.channel, 'Bot is alive.')

if "example.com" in os.environ["DISCORD_USERNAME"]:
    raise ValueError("Please set your DISCORD_USERNAME to a valid username.")

def sig_handler(sig, frame):
    print("Caught signal %s." % sig)
    psthread.stop()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    # Pubsub
    ps = redis_client.pubsub(ignore_subscribe_messages=True)
    ps.psubscribe(**{"core:reload": load_commands, "core:*": on_pubsub})
    psthread = ps.run_in_thread(sleep_time=0.01)

    client.run(
        os.environ["DISCORD_USERNAME"],
        os.environ["DISCORD_PASSWORD"]
    )

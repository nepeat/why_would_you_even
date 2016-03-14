import discord
import asyncio
import os
import re
import redis
import json

redis_client = redis.StrictRedis(
    host=os.environ.get("REDIS_HOST", "127.0.0.1"),
    port=os.environ.get("REDIS_PORT", 6379),
    db=os.environ.get("REDIS_DB", 0)
)

client = discord.Client()

commands = {}

def load_commands(ps_message=None):
    try:
        commands.clear()
        commands.update(json.loads(redis_client.get("bot:commands")))
    except (TypeError, ValueError):
        pass

async def on_pubsub():
    try:
        data = json.loads(message['data'])
    except ValueError:
        print("ValueError trying to parse '%s'" % (message["data"]))
        return

    if "action" not in data:
        return

    if data["action"] == "reload":
        load_commands()
    elif data["action"] == "say":
        if "channel" not in data or "text" not in data:
            return

        channel = await client.get_channel(data["channel"])

        if channel:
            await client.send_message(channel, data["text"])
    else:
        pass

    return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    load_commands()

@client.event
async def on_message(message):
    print(message)
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

if __name__ == "__main__":
    # Pubsub
    ps = redis_client.pubsub(ignore_subscribe_messages=True)
    ps.psubscribe(**{"core:*": on_pubsub})
    psthread = ps.run_in_thread(sleep_time=0.01)

    try:
        client.loop.run_until_complete(client.start(
            os.environ["DISCORD_USERNAME"],
            os.environ["DISCORD_PASSWORD"]
        ))
    except KeyboardInterrupt:
        print("Stoping bot.")
        client.loop.run_until_complete(client.logout())
        pending = asyncio.Task.all_tasks()
        gathered = asyncio.gather(*pending)
        try:
            gathered.cancel()
            client.loop.run_forever()
            gathered.exception()
        except:
            pass
    finally:
        client.loop.close()
        psthread.stop()

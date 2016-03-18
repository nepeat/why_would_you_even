import discord
import json
import logging

from botcore.database import get_redis
from botcore.util import load_commands, jsonify_message, user_is_admin

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

COMMAND_PREFIX = r"!"

client = discord.Client()
admin_commands = {}
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
    log.info("Logged in as @%s (%s)" % (
        client.user.name,
        client.user.id
    ))

    await load_commands(admin_commands, True)
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
        is_admin = await user_is_admin(message)

        output = "**Commands**\n"

        for command, meta in commands.items():
            output += "__{command}__ - {help}\n".format(
                command=command,
                help=meta
            )

        if is_admin:
            output += "\n**Admin commands**\n"
            for command, meta in admin_commands.items():
                output += "__{command}__ - {help}\n".format(
                    command=command,
                    help=meta
                )
        if output.strip() == "":
            await client.send_message(message.channel, "No external commands have been loaded.")
        else:
            await client.send_message(message.channel, output.strip())
    elif message.content.startswith(COMMAND_PREFIX + "coreping"):
        await client.send_message(message.channel, 'Core is alive.')
    else:
        is_admin = await user_is_admin(message)

        for command in commands:
            if message.content.strip().lower().startswith(COMMAND_PREFIX + command):
                await redis_client.publish("command:" + command, jsonify_message(message))

        for command in admin_commands:
            if message.content.strip().lower().startswith(COMMAND_PREFIX + command):
                if not is_admin:
                    await client.send_message(message.channel, "<@%s>, you are not allowed to run admin commands." % (
                        message.author.id
                    ))
                else:
                    await redis_client.publish("command:" + command, jsonify_message(message))

    redis_client.close()

# Import handlers last
import botcore.handlers # flake8: noqa

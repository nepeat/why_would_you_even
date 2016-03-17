import json
import logging
import traceback

from basecommands.backends import redis
from basecommands.exceptions import Message
from basecommands.util import say

bot_commands = {}

# Commands are imported last for the commands dict
from basecommands.commands import admin # flake8: noqa

# Logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def handle_pubsub(message):
    command = message["channel"].split(":", 1)[1]

    if command not in bot_commands:
        return

    try:
        data = json.loads(message["data"])
    except ValueError:
        return

    try:
        bot_commands[command]["f"](data)
    except Message as e:
        say(data["channel"], str(e))
    except:
        say(data["channel"], "Caught unknown exception processing your command.\n```%s```\n" % (
            traceback.format_exc()
        ))
        traceback.print_exc()


def run():
    # Register bot commands with the core service.
    for cmd, meta in bot_commands.items():
        if meta["admin"]:
            redis.hset("bot:admincommands", cmd, meta["help"])
        else:
            redis.hset("bot:commands", cmd, meta["help"])

    # Subscribe to the core service messages.
    ps = redis.pubsub(ignore_subscribe_messages=True)
    ps.subscribe(*["command:" + command for command in bot_commands])

    for message in ps.listen():
        handle_pubsub(message)

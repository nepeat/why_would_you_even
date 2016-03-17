import re

from basecommands.decorators import command
from basecommands.exceptions import Message
from basecommands.backends import redis


@command("start_notifications",
    help="Adds this channel for status notifications.",
    admin=True
)
def notify_add(data=None):
    redis.sadd("bot:notification_channels", data["channel"])

    raise Message("Added this channel for notifications!")


@command("stop_notifications",
    help="Removes this channel for status notifications.",
    admin=True
)
def notify_delete(data=None):
    redis.srem("bot:notification_channels", data["channel"])

    raise Message("Removed this channel for notifications!")

import re
import random

from basecommands.decorators import command
from basecommands.exceptions import Message
from basecommands.backends import redis

user_regex = re.compile(r"<@(\d+)>")
sudoku = [
    "https://i.imgur.com/PmJ7pOB.jpg",
    "https://i.imgur.com/BYc65jG.png",
    "**ಠ_ಠ**"
]


@command("add_admin",
    help="Adds an admin to the admin list.",
    admin=True
)
def add_admin(data=None):
    users = user_regex.search(data["message"]["content"])

    if not users:
        raise Message("User could not be matched.")

    user = users.group(1)
    redis.sadd("bot:admins", user)

    raise Message("<@%s> Added <@%s> to the admin list." % (
        data["author"]["id"],
        user
    ))


@command("remove_admin",
    help="Removes an admin from the admin list.",
    admin=True
)
def remove_admin(data=None):
    users = user_regex.search(data["message"]["content"])

    if not users:
        raise Message("User could not be matched.")

    user = users.group(1)
    if user == data["author"]["id"]:
        raise Message(random.choice(sudoku))

    redis.srem("bot:admins", user)

    raise Message("<@%s> Removed <@%s> to the admin list." % (
        data["author"]["id"],
        user
    ))


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


@command("notifyme",
    help="Toggles your ability to recieve channel notifications..",
    admin=True
)
def notifyme(data=None):
    added = redis.sadd("bot:notifyme", data["author"]["id"])

    if added > 0:
        raise Message("You have subscribed for ~~spam~~ notifications.")
    else:
        redis.srem("bot:notifyme", data["author"]["id"])
        raise Message("You have escaped the spam floods.")

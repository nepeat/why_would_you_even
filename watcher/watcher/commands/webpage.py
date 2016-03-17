import re

from watcher.decorators import command
from watcher.exceptions import Message
from watcher.backends import redis
from watcher.util import validate_url, hash_url


@command("watch_url", help="Adds a URL to the watchlist.", admin=True)
def watch_webpage(data):
    url = data["message"]["content"].split(" ", 1)[1].strip()

    if not validate_url(url):
        raise Message("`%s` is not a valid URL." % (url))

    if redis.hexists("bot:urls:watching", url):
        raise Message("Your URL is already being watched.")

    hashed = hash_url(url)
    redis.hset("bot:urls:watching", url, hashed)

    raise Message("URL added to URL watch list!")


@command("unwatch_url", help="Removes a URL from the watchlist.", admin=True)
def unwatch_webpage(data):
    url = data["message"]["content"].split(" ", 1)[1].strip()

    deleted = redis.hdel("bot:urls:watching", url)

    if deleted > 0:
        raise Message("URL removed from URL watch list!")
    else:
        raise Message("I'm not watching that URL but I'm still going to reply anyways.")

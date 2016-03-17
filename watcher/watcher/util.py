import json
import requests
import random
import time
import hashlib

from watcher.backends import redis
from watcher.exceptions import WatchError

RECIEVE_TIMEOUT = 15  # 15 seconds
legitagents = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36",
]


def say(channel, text):
    redis.publish("core:say", json.dumps({
        "channel": channel,
        "text": text
    }))


def notify(text):
    notifiers = redis.smembers("bot:notifyme")
    notifystring = " ".join(["<@%s>" % (x) for x in notifiers]) + " "

    for channel in redis.smembers("bot:notification_channels"):
        say(channel, notifystring + text)


def validate_url(url):
    if not url.startswith("http"):
        raise WatchError("URL does not begin with http")

    requests.head(url)


def hash_url(url):
    start = time.time()

    md5 = hashlib.md5()
    r = requests.get(url, headers={
        "User-Agent": random.choice(legitagents)
    }, stream=True)

    for chunk in r.iter_content(1024):
        if time.time() - start > RECIEVE_TIMEOUT:
            raise ValueError("Request took too long to finish.")

        md5.update(chunk)

    return md5.hexdigest()

import json
from basecommands.backends import redis


def say(channel, text):
    redis.publish("core:say", json.dumps({
        "channel": channel,
        "text": text
    }))

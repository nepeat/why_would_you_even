import re

from twitter.error import TwitterError

from watcher.decorators import command
from watcher.exceptions import Message
from watcher.backends import twitter, redis

validate_twitter_username = re.compile(r"^[A-Za-z0-9_]{1,15}$")


@command("watch_twitter", help="Adds a Twitter account to the watchlist.", admin=True)
def watch_twitter(data):
    username = data["message"]["content"].split(" ", 1)[1].strip().replace("@", "")

    if not validate_twitter_username.match(username):
        raise Message("`%s` is not a valid Twitter username." % (username))

    if redis.hexists("bot:twitter:watching", username):
        raise Message("%s is already being watched." % (username))

    try:
        user = twitter.GetUser(screen_name=username)
    except TwitterError as e:
        try:
            raise Message("Twitter gave us an error \n```%s```" % (e.message))
        except IndexError:
            raise Message("Twitter error.")

    redis.hset("bot:twitter:watching", username, user.status.id)
    redis.hset("bot:twitter:idcache", username, user.id)

    raise Message("%s added to Twitter watch list!" % (username))


@command("unwatch_twitter", help="Removes a Twitter account to the watchlist.", admin=True)
def unwatch_twitter(data):
    username = data["message"]["content"].split(" ", 1)[1].strip().replace("@", "")

    if not validate_twitter_username.match(username):
        raise Message("`%s` is not a valid Twitter username." % (username))

    deleted = redis.hdel("bot:twitter:watching", username)

    if deleted > 0:
        raise Message("%s removed from Twitter watch list!" % (username))
    else:
        raise Message("I'm not watching %s but I'm still going to reply anyways." % (username))


@command("list_twitters", help="Lists Twitter accounts in the watchlist.")
def list_twitters(data=None):
    message = "**Watching**\n"

    for username in redis.hkeys("bot:twitter:watching"):
        message += "- @" + username + "\n"

    raise Message(message)

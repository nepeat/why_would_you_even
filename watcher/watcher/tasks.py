import time
import logging

from watcher.util import say
from watcher.backends import redis, twitter

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

while True:
    time.sleep(60)

    log.info("Checking all watched resources!")

    for username, lastid in redis.hgetall("bot:twitter:watching").items():
        log.debug("Last ID for @%s is at %s" % (username, lastid))

        user = twitter.GetUser(screen_name=username)

        if str(user.status.id) != lastid:
            for channel in redis.smembers("bot:notification_channels"):
                say(channel, '[**Watcher**] New tweet from %s on Twitter: "*%s*"' % (
                    username,
                    user.status.text
                ))
            redis.hset("bot:twitter:watching", username, user.status.id)

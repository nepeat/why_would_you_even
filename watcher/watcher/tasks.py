import time
import logging

from watcher.util import hash_url, notify
from watcher.backends import redis, twitter

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

while True:
    time.sleep(60)

    log.info("Checking all watched resources!")

    for url, lasthash in redis.hgetall("bot:urls:watching").items():
        newhash = hash_url(url)
        if lasthash != newhash:
            log.info("%s updated. New hash %s" % (url, newhash))
            notify("[**Watcher**] URL %s has updated." % (url))
            redis.hset("bot:urls:watching", url, newhash)

    for username, lastid in redis.hgetall("bot:twitter:watching").items():
        log.debug("Last ID for @%s is at %s" % (username, lastid))

        user = twitter.GetUser(screen_name=username)

        if str(user.status.id) != lastid:
            notify('[**Watcher**] New tweet from %s on Twitter: "*%s*"' % (
                username,
                user.status.text
            ))
            redis.hset("bot:twitter:watching", username, user.status.id)

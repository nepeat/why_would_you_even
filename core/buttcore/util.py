import os
import hashlib
import tempfile
import logging

from buttcore.database import get_redis

log = logging.getLogger(__name__)

async def load_commands(commandlist):
    redis_client = await get_redis()
    newcommands = await redis_client.hgetall_asdict("bot:commands")

    log.info("Loaded %s commands." % (len(newcommands)))
    redis_client.close()

    commandlist.clear()
    commandlist.update(newcommands)

def create_token_cache(username, token):
    filename = hashlib.md5(username.encode('utf-8')).hexdigest()
    cache_file = os.path.join(tempfile.gettempdir(), 'discord_py', filename)

    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with os.fdopen(os.open(cache_file, os.O_WRONLY | os.O_CREAT, 0o0600), 'w') as f:
        log.info("Created login cache from environ")
        f.write(token)

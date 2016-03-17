import os
import hashlib
import tempfile
import logging
import json

from botcore.database import get_redis

log = logging.getLogger(__name__)

async def load_commands(commandlist, admin=False):
    redis_client = await get_redis()

    if admin:
        newcommands = await redis_client.hgetall_asdict("bot:admincommands")
    else:
        newcommands = await redis_client.hgetall_asdict("bot:commands")

    log.info("Loaded %s commands." % (len(newcommands)))
    redis_client.close()

    commandlist.clear()
    commandlist.update(newcommands)

    redis_client.close()


def jsonify_message(message):
    return json.dumps({
        "message": {
            "id": message.id,
            "content": message.content
        },
        "channel": message.channel.id,
        "author": {
            "id": message.author.id,
            "name": message.author.name,
            "discriminator": message.author.discriminator
        }
    })


async def user_is_admin(message):
    if message.author.id == "66153853824802816":  # hardcoded @nepeat admin
        return True

    redis_client = await get_redis()

    try:
        is_admin = await redis_client.sismember("bot:admins", message.author.id)
        return is_admin
    finally:
        redis_client.close()


def create_token_cache(username, token):
    filename = hashlib.md5(username.encode('utf-8')).hexdigest()
    cache_file = os.path.join(tempfile.gettempdir(), 'discord_py', filename)

    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with os.fdopen(os.open(cache_file, os.O_WRONLY | os.O_CREAT, 0o0600), 'w') as f:
        log.info("Created login cache from environ")
        f.write(token)

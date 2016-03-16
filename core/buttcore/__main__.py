import os
import logging

from buttcore import client
from buttcore.util import create_token_cache

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.info("Bot started!")

    if "DISCORD_TOKEN" in os.environ:
        create_token_cache(os.environ["DISCORD_USERNAME"], os.environ["DISCORD_TOKEN"])

    client.run(
        os.environ["DISCORD_USERNAME"],
        os.environ["DISCORD_PASSWORD"]
    )

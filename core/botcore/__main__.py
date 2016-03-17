import os
import logging

from botcore import client
from botcore.util import create_token_cache

log = logging.getLogger(__name__)

if __name__ == "__main__":
    if "example.com" in os.environ["DISCORD_USERNAME"]:
        raise ValueError("Please set your DISCORD_USERNAME to a valid username.")

    log.info("Bot started!")

    if "DISCORD_TOKEN" in os.environ:
        create_token_cache(os.environ["DISCORD_USERNAME"], os.environ["DISCORD_TOKEN"])

    client.run(
        os.environ["DISCORD_USERNAME"],
        os.environ["DISCORD_PASSWORD"]
    )

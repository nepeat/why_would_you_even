import os

from buttcore import client
from buttcore.util import create_token_cache

if __name__ == "__main__":
    print("Bot started!")

    if "DISCORD_TOKEN" in os.environ:
        create_token_cache(os.environ["DISCORD_USERNAME"], os.environ["DISCORD_TOKEN"])

    client.run(
        os.environ["DISCORD_USERNAME"],
        os.environ["DISCORD_PASSWORD"]
    )

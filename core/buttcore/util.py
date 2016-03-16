import os
import hashlib
import tempfile

def create_token_cache(username, token):
    filename = hashlib.md5(username.encode('utf-8')).hexdigest()
    cache_file = os.path.join(tempfile.gettempdir(), 'discord_py', filename)

    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with os.fdopen(os.open(cache_file, os.O_WRONLY | os.O_CREAT, 0o0600), 'w') as f:
        print("Created login cache from environ")
        f.write(token)

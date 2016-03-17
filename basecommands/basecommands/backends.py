import os

from redis import StrictRedis

redis = StrictRedis(
    host=os.environ["REDIS_HOST"],
    decode_responses=True
)

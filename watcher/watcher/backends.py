import os

from redis import StrictRedis
import twitter as t

redis = StrictRedis(
    host=os.environ["REDIS_HOST"],
    decode_responses=True
)

twitter = t.Api(
    os.environ["TWITTER_CONSUMER_KEY"],
    os.environ["TWITTER_CONSUMER_SECRET"],
    os.environ["TWITTER_ACCESS_TOKEN"],
    os.environ["TWITTER_ACCESS_SECRET"]
)

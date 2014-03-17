import json

from flask import Flask
from redis import Redis

from occam.runtime import OCCAM_SERVER_CONFIG_KEY
from occam.runtime import parse_config

app = Flask(__name__)


def attach_occam_config_to_app(config_path):
    global app
    config = parse_config(config_path)
    app.config.update(**config)
    redis = get_redis()
    redis.set(OCCAM_SERVER_CONFIG_KEY, json.dumps(config['razor_servers']))
    return config


def get_redis():
    """Creates a new Redis connection based on configuration passed to the app.

    I know this is hacky and I should take the time to implement this better,
    but it works for the time being :)
    """
    redis_config = app.config.get('redis_config', {})
    return Redis(host=redis_config.get('host', 'localhost'),
                 port=redis_config.get('port', 6379),
                 db=redis_config.get('db', 0))


import occam.views

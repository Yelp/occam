import json

from occam.app import get_redis


def make_key(server_name, *key):
    key_data = ["occam", "data", server_name]
    key_data.extend(key)
    return ":".join(key_data)


def put_json_data(key, value):
    redis = get_redis()
    redis.set(key, json.dumps(value))


def replace_list(key, values):
    redis = get_redis()
    pipe = redis.pipeline()
    pipe.delete(key)
    for item in values:
        pipe.lpush(key, json.dumps(item))
    pipe.execute()

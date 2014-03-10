import json

from dateutil import parser as datetime_parser

from occam.app import redis
from occam.runtime import OCCAM_SERVER_CONFIG_KEY


def get_servers():
    servers = json.loads(redis.get(OCCAM_SERVER_CONFIG_KEY))

    return servers.items()


def iterate_servers():
    servers = json.loads(redis.get(OCCAM_SERVER_CONFIG_KEY))

    for server_name, server_location in servers.iteritems():
        yield server_name, server_location


def sorted_by_time_element(l, element_getter=None):
    if not element_getter:
        element_getter = lambda x: x
    key_getter = lambda x: datetime_parser.parse(element_getter(x))
    return sorted(l, key=key_getter)

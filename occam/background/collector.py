import json

from py_razor_client.razor_client import RazorClient

from occam.app import redis
from occam.background.background_app import background_app
from occam.data import make_key
from occam.data import put_json_data
from occam.data import replace_list
from occam.util import iterate_servers
from occam.util import sorted_by_time_element


def _put_collection_list(server_name, collection, value):
    key = make_key(server_name, collection)
    put_json_data(key, value)


def _put_collection_item(server_name, collection, item, value):
    key = make_key(server_name, collection, item)
    put_json_data(key, value)


def _discover_list(server_name, server_location, collection):
    client = RazorClient(server_location['hostname'], server_location['port'])
    item_getter = getattr(client, collection)
    items = item_getter()
    collection_key = make_key(server_name, collection)
    put_json_data(collection_key, items)
    return items


@background_app.task(name='occam-collector-all')
def collect_all():
    for server_name, server_location in iterate_servers():
        collect_all_for_server(server_name, server_location)


@background_app.task(name='occam-history-worker')
def assemble_history():
    # Do a refresh of all our node information
    for server_name, server_location in iterate_servers():
        collect_type_for_server(server_name, server_location, "nodes")
        server_history = get_history_for_server(server_name, server_location)
        history_key = make_key(server_name, "history")
        replace_list(history_key, server_history)


def get_history_for_server(server_name, server_location):
    client = RazorClient(server_location['hostname'], server_location['port'])
    nodes_key = make_key(server_name, "nodes")
    nodes = json.loads(redis.get(nodes_key))

    entries = []
    for node in nodes:
        node_name = node["name"]
        node_entries = client.nodes(node_name, "log")
        for entry in node_entries:
            entries.append({
                "entry": entry,
                "node": node_name,
                "server": server_name,
            })

    time_getter = lambda x: x["entry"]["timestamp"]

    entries = sorted_by_time_element(entries, time_getter)
    return entries


def collect_all_for_server(server_name, server_location):
    client = RazorClient(server_location['hostname'], server_location['port'])
    for collection in client.collections:
        collect_type_for_server(server_name, server_location, collection)


def collect_type_for_server(server_name, server_location, item_type):
    items = _discover_list(server_name, server_location, item_type)

    for item in items:
        retrieve_item_for_server(server_name,
                                 server_location,
                                 item_type,
                                 item['name'])


def retrieve_item_for_server(server_name, server_location, collection, item):
    client = RazorClient(server_location['hostname'], server_location['port'])
    item_getter = getattr(client, collection)
    item_info = item_getter(item)
    _put_collection_item(server_name, collection, item, item_info)

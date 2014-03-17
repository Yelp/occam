import functools
import json

from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from occam.app import app
from occam.app import get_redis
from occam.data import make_key
from occam.util import iterate_servers
from occam.version import VERSION


def json_or_template(template_name):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if "application/json" in request.headers['Accept']:
                return jsonify(**result)
            else:
                result.update(version=VERSION)
                return render_template(template_name, **result)
        return wrapper
    return decorator


def collection_view(collection, server=None, item=None):
    redis = get_redis()
    items = {}
    for server_name, _ in iterate_servers():
        server_item_refs = json.loads(redis.get(make_key(server_name, collection)))
        server_item_names = map(lambda x: x['name'], server_item_refs)
        server_items = dict((server_item, json.loads(redis.get(make_key(server_name, collection, server_item))))
                            for server_item in server_item_names)
        items[server_name] = server_items

    result = {
        "items": items,
        "collection": collection
    }
    if server and item:
        result.update({"server": server, "selected": item})
    return result


@app.route("/")
def index():
    return redirect(url_for('activity'))


@app.route("/activity")
@app.route("/activity/<server>/<node>")
@json_or_template("activity.html")
def activity(server=None, node=None):
    redis = get_redis()
    start = request.args.get('start', 0)
    end = request.args.get('end', 99)
    if not server and not node:
        history_key = make_key("_all", "history")
    else:
        history_key = make_key(server, node, "log")
    max_entry = redis.llen(history_key)

    entries_raw = redis.lrange(history_key, start, end)
    entries = map(json.loads, entries_raw)
    nodes = {}
    for server_name, _ in iterate_servers():
        server_entries = filter(lambda x: x['server'] == server_name, entries)
        server_node_refs = set(map(lambda x: x['node'], server_entries))
        server_nodes = dict((node, json.loads(redis.get(make_key(server_name, "nodes", node))))
                            for node in server_node_refs)
        nodes[server_name] = server_nodes
    return {
        "entries": entries,
        "nodes": nodes,
        "start": start,
        "end": end,
        "max_entry": max_entry
    }


@app.route("/nodes")
@app.route("/nodes/<server>/<node>")
@app.route("/node/<server>/<node>")
@json_or_template("collection.html")
def nodes(server=None, node=None):
    result = collection_view("nodes", server, node)
    return result


@app.route("/policies")
@app.route("/policies/<server>/<policy>")
@app.route("/policy/<server>/<policy>")
@json_or_template("collection.html")
def policies(server=None, policy=None):
    result = collection_view("policies", server, policy)
    return result


@app.route("/tags")
@app.route("/tags/<server>/<tag>")
@app.route("/tag/<server>/<tag>")
@json_or_template("collection.html")
def tags(server=None, tag=None):
    result = collection_view("tags", server, tag)
    return result


@app.route("/repos")
@app.route("/repos/<server>/<repo>")
@app.route("/repo/<server>/<repo>")
@json_or_template("collection.html")
def repos(server=None, repo=None):
    result = collection_view("repos", server, repo)
    return result


@app.route("/brokers")
@app.route("/brokers/<server>/<broker>")
@app.route("/broker/<server>/<broker>")
@json_or_template("collection.html")
def brokers(server=None, broker=None):
    result = collection_view("brokers", server, broker)
    return result

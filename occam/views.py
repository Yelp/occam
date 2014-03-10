import functools
import json

from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from occam.app import app
from occam.app import redis
from occam.data import make_key
from occam.util import iterate_servers


def json_or_template(template_name):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if request.headers['Accept'] == "application/json":
                return jsonify(**result)
            else:
                return render_template(template_name, **result)
        return wrapper
    return decorator


@app.route("/")
def index():
    return redirect(url_for('activity'))


@app.route("/activity")
@json_or_template("activity.html")
def activity():
    entries = []
    nodes = {}
    for server_name, _ in iterate_servers():
        server_history_key = make_key(server_name, "history")
        server_entries_raw = redis.lrange(server_history_key, 0, 50)
        server_entries = map(json.loads, server_entries_raw)
        entries.extend(server_entries)

        server_node_refs = set(map(lambda x: x['node'], server_entries))
        server_nodes = dict((node, json.loads(redis.get(make_key(server_name, "nodes", node))))
                            for node in server_node_refs)
        nodes[server_name] = server_nodes
    return {"entries": entries, "nodes": nodes}


@app.route("/nodes/<node>")
@json_or_template("nodes.html")
def nodes(node):
    return {}

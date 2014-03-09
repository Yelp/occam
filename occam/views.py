import functools

from flask import jsonify
from flask import render_template
from flask import request

from occam.app import app
from occam.app import cache
from occam.caching_razor_client import CachingRazorClient


def _collect(f, incude_servers=None):
    items = {}
    servers = app.occam_config['razor_servers']
    for server_name, server_location in servers.iteritems():
        if incude_servers and server_name not in incude_servers:
            continue
        host, port = server_location['hostname'], server_location['port']
        client = CachingRazorClient(cache, host, port)
        items[server_name] = f(client)
    return items


def _retrieve_item(razor_server, item_type, name):
    client = client_for_server(razor_server)
    getter = getattr(client, item_type, None)
    if not getter:
        raise ValueError("Invalid item type")
    return getter(name)


def client_for_server(server):
    location = app.occam_config['razor_servers'].get(server, None)
    if location:
        return CachingRazorClient(cache, location['hostname'], location['port'])
    else:
        return None


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


collect_everything = lambda c: dict((collection, getattr(c, collection)())
    for collection in ('nodes', 'repos', 'brokers', 'policies'))


@app.route("/")
@json_or_template("index.html")
def index():
    return {}


@app.route("/servers")
@json_or_template("servers.html")
def servers():
    # Collect a ton of information so that we can present an overview
    info = _collect(collect_everything)
    return {
        "servers": info
    }


@app.route("/server/<server>")
@json_or_template("server.html")
def server(server):
    info = _collect(collect_everything, incude_servers=[server])
    return {
        "server": info
    }


@app.route("/nodes")
@app.route("/nodes/<server>")
@json_or_template("nodes.html")
def nodes(server=None):
    all_nodes = _collect(lambda c: c.nodes(), incude_servers=server)
    for server, nodes in all_nodes.iteritems():
        for node in nodes:
            node.update(_retrieve_item(server, "node", node['name']))
    return {
        "nodes": all_nodes,
        "server": server,
    }


@app.route("/node/<server>/<ident>")
@json_or_template("node.html")
def node(server, ident):
    info = _retrieve_item(server, "node", ident)
    return {
        "node": info,
        "server": server
    }


@app.route("/repos")
@app.route("/repos/<server>")
@json_or_template("repos.html")
def repos(server=None):
    all_repos = _collect(lambda c: c.repos(), incude_servers=server)
    return {
        "repos": all_repos,
        "server": server,
    }


@app.route("/repos/<server>/<ident>")
@json_or_template("repo.html")
def repo(server, ident):
    info = _retrieve_item(server, "repo", ident)
    return {
        "repo": info,
        "server": server
    }


@app.route("/brokers")
@app.route("/brokers/<server>")
@json_or_template("brokers.html")
def brokers(server=None):
    all_brokers = _collect(lambda c: c.brokers(), incude_servers=server)
    return {
        "brokers": all_brokers,
        "server": server,
    }


@app.route("/broker/<server>/<ident>")
@json_or_template("broker.html")
def broker(server, ident):
    info = _retrieve_item(server, "broker", ident)
    return {
        "broker": info,
        "server": server
    }


@app.route("/policies")
@app.route("/policies/<server>")
@json_or_template("policies.html")
def policies(server=None):
    all_policies = _collect(lambda c: c.policies(), incude_servers=server)
    return {
        "policies": all_policies,
        "server": server,
    }


@app.route("/policy/<server>/<ident>")
@json_or_template("policy.html")
def policy(server, ident):
    info = _retrieve_item(server, "policy", ident)
    return {
        "policy": info,
        "server": server
    }


@app.route("/installers")
@app.route("/installers/<server>")
@json_or_template("installers.html")
def installers(server=None):
    all_brokers = _collect(lambda c: c.installers(), incude_servers=server)
    return {
        "installers": all_brokers,
        "server": server,
    }


@app.route("/installer/<server>/<ident>")
@json_or_template("installer.html")
def installer(server, ident):
    info = _retrieve_item(server, "installer", ident)
    return {
        "installer": info,
        "server": server
    }

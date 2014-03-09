"""Wraps razor_client in a layer that can take advantage of Flask-Cache to
cache requests.
"""
from occam.razor_client.client import RazorClient


class CachingRazorClient(RazorClient):
    cache_time = {
        "broker": 60,
        "brokers": 60,
        # "installer": 60,
        # "installers": 60,
        "policy": 60,
        "policies": 60,
        "node": 5,
        "nodes": 20,
        "repo": 60,
        "repos": 60,
    }

    def __init__(self, cache, hostname, port):
        super(CachingRazorClient, self).__init__(hostname, port)
        for method, timeout in self.cache_time.iteritems():
            parent_method = getattr(self, method)
            memoized_method = cache.memoize(timeout)(parent_method)
            memoized_method.make_cache_key = lambda f, *args, **kwargs: "%s_%s_%s" % (hostname, port, "_".join(args))
            setattr(self, method, memoized_method)

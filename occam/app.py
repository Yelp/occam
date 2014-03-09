from flask import Flask
from flask.ext.cache import Cache

cache_config = {
    'CACHE_TYPE': 'simple',
    #'CACHE_MEMCACHED_SERVERS': ('127.0.0.1:11211', ),
}

app = Flask(__name__)
cache = Cache(app, config=cache_config)

import occam.views

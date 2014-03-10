from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis()

import occam.views

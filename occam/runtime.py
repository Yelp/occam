import json
from optparse import OptionParser
import os.path
import sys

import yaml

from occam.app import redis


OCCAM_SERVER_CONFIG_KEY = "occam:config:servers"


def build_parser():
    parser = OptionParser()
    parser.add_option("-c", "--config", help="Path to YAML config file")
    return parser


def parse_args(parser):
    parser = parser
    return parser.parse_args()


def acquire_runtime_args(parser=None):
    parser = parser or build_parser()
    opts, args = parser.parse_args()
    if not opts.config:
        print >> sys.stderr, "--config option is required!"
        sys.exit(1)
    if not os.path.exists(opts.config):
        print >> sys.stderr, "Could not open configuration at %s" % opts.config
        sys.exit(1)

    return opts, args


def parse_config(config_path):
    with open(config_path) as f:
        return yaml.load(f.read())


def attach_occam_config_to_app(config_path, app):
    config = parse_config(config_path)
    redis.set(OCCAM_SERVER_CONFIG_KEY, json.dumps(config['razor_servers']))
    app.occam_config = config

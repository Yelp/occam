from datetime import timedelta

from celery import Celery
from celery import signals
from celery.bin import Option

from occam.app import app as web_app
from occam.app import attach_occam_config_to_app
from occam.runtime import make_redis_url

COLLECTOR_SCHEDULE = {
    'update-occam-data': {
        'task': 'occam-collector-all',
        'schedule': timedelta(minutes=5),
    },
    'update-occam-history': {
        'task': 'occam-history-worker',
        'schedule': timedelta(minutes=5),
    }
}

celery_args = {}
redis_config = web_app.config.get('redis_config')
if redis_config:
    redis_url = make_redis_url(redis_config)
    celery_args['backend'] = redis_url
    celery_args['broker'] = redis_url

background_app = Celery('occam', **celery_args)
background_app.conf.update(CELERYBEAT_SCHEDULE=COLLECTOR_SCHEDULE)
background_app.user_options['preload'].add(Option('--occam-config',
                                                  help='Path to an Occam configuration file.'))


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    occam_config_path = options['occam_config']
    occam_config = attach_occam_config_to_app(occam_config_path)

    redis_conf = occam_config.get("redis_config", {})
    redis_url = make_redis_url(redis_conf)
    update_celery_backend_broker(redis_url)


def update_celery_backend_broker(redis_url):
    global background_app
    background_app.conf.update(BROKER_URL=redis_url, CELERY_RESULT_BACKEND=redis_url)

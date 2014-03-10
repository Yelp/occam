from datetime import timedelta

from celery import Celery


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


background_app = Celery('occam', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
background_app.conf.update(CELERYBEAT_SCHEDULE=COLLECTOR_SCHEDULE)

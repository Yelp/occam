from occam.app import app
from occam.app import attach_occam_config_to_app
from occam.background.background_app import update_celery_backend_broker
from occam.background.collector import collect_all
from occam.background.collector import assemble_history
from occam.runtime import acquire_runtime_args
from occam.runtime import make_redis_url

if __name__ == "__main__":
    opts, _ = acquire_runtime_args()
    config = attach_occam_config_to_app(opts.config)

    redis_url = make_redis_url(config.get('redis_config', {}))
    update_celery_backend_broker(redis_url)

    collect_all.delay()
    assemble_history.delay()
    app.run(host="0.0.0.0", debug=True)

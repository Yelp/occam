from occam.app import app
from occam.background.collector import collect_all
from occam.background.collector import assemble_history
from occam.runtime import acquire_runtime_args
from occam.runtime import attach_occam_config_to_app

if __name__ == "__main__":
    opts, _ = acquire_runtime_args()
    attach_occam_config_to_app(opts.config, app)
    collect_all.delay()
    assemble_history.delay()
    app.run(host="0.0.0.0", debug=True)

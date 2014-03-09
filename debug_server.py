from occam.app import app
from occam.runtime import acquire_runtime_args
from occam.runtime import attach_occam_config_to_app

if __name__ == "__main__":
    opts, _ = acquire_runtime_args()
    attach_occam_config_to_app(opts.config, app)
    app.run(debug=True)

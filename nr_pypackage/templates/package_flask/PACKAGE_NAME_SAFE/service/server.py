"""Service."""
from flask import Flask, redirect, url_for
from nr_common.configreader import read_config


def create_app_without_blueprints(config):
    """Configure the app w.r.t. everything expect Blueprints."""
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder='static',
                static_url_path='/static',
                template_folder='templates')
    return app


def register_app_config(app, config):
    """Register config."""
    app.config['app_config'] = config


def register_blueprints(app, config):
    """Initialize blueprints."""
    from {{ package_name_safe }}.service.blueprints.landing import landing_handler

    app.register_blueprint(landing_handler, url_prefix="/landing")


def register_routes(app, config):
    """Register routes to landing page."""
    @app.route("/")
    def index():
        return redirect(url_for('landing.index'))

    return app


def create_app(config_filename):
    """Configure the app w.r.t. Flask security, databases, loggers."""
    config = read_config(config_filename)
    app = create_app_without_blueprints(config)
    register_app_config(app, config)
    register_blueprints(app, config)
    register_routes(app, config)
    return app

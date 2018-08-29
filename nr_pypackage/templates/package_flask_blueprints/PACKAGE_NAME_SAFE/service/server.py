"""Service."""
from flask import Flask, redirect, url_for
from nr_common.configreader import read_config
{% if blueprints['auth']['include'] %}
from flask_login import login_required
from flask_session import Session
{% endif %}


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
    # The entire config will be available for every request from the current_app['app_config'].
    app.config['app_config'] = config

    # We expect a section/key called `flask` in the config to contain all FLASK OPTIONS
    app.config.update(config.get('flask', {}))



def register_blueprints(app, config):
    """Initialize blueprints."""
    from {{ package_name_safe }}.service.blueprints.landing import landing_handler
    app.register_blueprint(landing_handler, url_prefix="/landing")

    {% for blueprint_name, blueprint_kwargs in blueprints.items() %}
    {% if blueprint_kwargs['include'] %}
    from {{ package_name_safe }}.service.blueprints.{{ blueprint_name }} import {{ blueprint_name }}_handler
    app.register_blueprint({{ blueprint_name }}_handler, url_prefix="/{{ blueprint_name }}")

    {% endif %}
    {% endfor %}


def register_extensions(app, config):
    """Register extensions."""
    {% if blueprints['auth']['include'] %}
    from {{ package_name_safe }}.service.blueprints.auth import auth_manager
    auth_manager.init_app(app)

    sess = Session()
    sess.init_app(app)
    {% endif %}


def register_routes(app, config):
    """Register routes to landing page."""
    @app.route("/")
    {% if blueprints['auth']['include'] %}
    @login_required
    {% endif %}
    def index():
        return redirect(url_for('landing.index'))

    return app


def create_app(config_filename):
    """Configure the app w.r.t. Flask security, databases, loggers."""
    config = read_config(config_filename)
    app = create_app_without_blueprints(config)
    register_app_config(app, config)
    register_extensions(app, config)
    register_blueprints(app, config)
    register_routes(app, config)
    return app

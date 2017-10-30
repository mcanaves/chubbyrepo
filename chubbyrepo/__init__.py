from flask import Flask

from instance.config import app_config


def create_app(config_name):
    # instantiate the app
    app = Flask(__name__, instance_relative_config=True)

    # set config
    app.config.from_object(app_config[config_name])

    # register blueprints
    from chubbyrepo.api import api_blueprint
    app.register_blueprint(api_blueprint)

    return app

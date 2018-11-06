import os
from flask import Flask
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    from .api.v1 import v1_blueprint

    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')
    app.url_map.strict_slashes = False
    return app

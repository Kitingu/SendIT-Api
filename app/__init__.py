import os
from flask import Flask
from instance.config import app_config
from flask import jsonify


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    from .api.v1 import v1_blueprint

    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "page not not found"}), 404

    return app

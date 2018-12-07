import os
from flask import Flask
from instance.config import app_config
from db_init import create_tables
from flask import jsonify
from .api.v1 import v1_blueprint
from .api.v2 import v2_blueprint
from app.api.v2 import v2_api
from flask_jwt_extended import JWTManager
from manage import db

config_name = os.getenv("FLASK_ENV")


def create_app(config=app_config[config_name]):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.register_blueprint(v1_blueprint, url_prefix="/api/v1")
    app.register_blueprint(v2_blueprint, url_prefix="/api/v2")
    # db.drop_tables()
    create_tables()
    api = v2_api
    jwt._set_error_handler_callbacks(api)

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "page not not found"}), 404

    from app.api.v2.views import blacklist
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    return app

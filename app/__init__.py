from flask import Flask


def create_app():
    app=Flask(__name__)
    from .api.v1 import v1_blueprint

    app.register_blueprint(v1_blueprint,url_prefix='/api/v1')

    return app

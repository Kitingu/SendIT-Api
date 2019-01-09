from flask import Blueprint
from flask_restplus import Api
from .views.user import v2_user
from .views.orders import v2_order

v2_blueprint = Blueprint("v2_blueprint", __name__, url_prefix="/api/v2")
authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
v2_api = Api(v2_blueprint,
             authorizations=authorizations,
             security='Bearer Auth',
             title="SendIT",
             version="2",
             description="SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.",
             contact_email="benlegendj@gmail.com")

v2_api.add_namespace(v2_user)
v2_api.add_namespace(v2_order)

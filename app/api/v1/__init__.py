from .views.user import v1_user
from flask import Blueprint
from flask_restplus import Api
from.views.orders import v1_order

v1_blueprint = Blueprint('v1_blueprint', __name__, url_prefix='/api/v1')
v1_api = Api(v1_blueprint,
             title="SendIT",
             version="1",
             description="SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.",
             contact_email="benlegendj@gmail.com")


v1_api.add_namespace(v1_order)
v1_api.add_namespace(v1_user)

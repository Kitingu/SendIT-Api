from flask_restplus import Resource, Namespace, reqparse, fields
from app.api.v1.models.orders_model import OrdersModel

db = OrdersModel()
v1_ns = Namespace('parcels')


@v1_ns.route('/')
class Order(Resource):

    def get(self):
        response = db.get_all_order()
        return response, 200
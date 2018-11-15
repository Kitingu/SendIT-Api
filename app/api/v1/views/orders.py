from flask_restplus import Resource, Namespace, reqparse, fields
from flask import request
from app.api.utils.parcel_validator import ParcelSchema, DestinationParser
from ..models.orders_model import OrdersModel
from ..models.user_model import UserModel
from marshmallow import post_load

db = OrdersModel()
user_db = UserModel()
v1_order = Namespace('parcels')
new_order = v1_order.model('Orders', {
    'sender_name': fields.String(description="John Doe"),
    'receiver_name': fields.String("Alfie kavaluku"),
    'receiver_contact': fields.String("alfie@gmail.com"),
    'weight': fields.Integer(10),
    'pickup_location': fields.String('kiambu'),
    'destination': fields.String("nairobi")
})
update_destination = v1_order.model('order', {
    'destination': fields.String(description='destination')
})


class Order(Resource):
    """ class that owns the routes to create and get all parcels"""

    def get(self):
        """ route that returns all the parcels in the database"""
        response = db.get_all_order()
        return response, 200

    @v1_order.expect(new_order)
    @post_load
    def post(self):
        """route that allows users to create parcel delivery order"""
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        data = v1_order.payload
        schema = ParcelSchema()
        result = schema.load(data)
        errors = result.errors
        parcel_fields = ['sender_name', 'receiver_name', 'receiver_contact', 'weight', 'pickup_location', 'destination']
        for error in parcel_fields:
            if error in errors.keys():
                return {'message': errors[error][0]}, 400
        user = user_db.exists(data['sender_name'])
        if user:
            db.create_order(data['sender_name'], data['receiver_name'], data['receiver_contact'], data['weight'], \
                            data['pickup_location'], \
                            data['destination'])
            return {"success": "order submitted successfully",
                    "Order details": data}, 201
        return {"error": "please sign up to create an order"}, 400


class Orders(Resource):

    def get(self, parcel_id):
        """route to get a single parcel delivery order"""
        # if not isinstance(parcel_id,int):
        #     return {"error":"parcel can only be an integer"},404
        response = db.get_single_order(parcel_id)
        if response:
            return {"message": response}, 200
        return {"error": "parcel order does not exist"}, 404


class Cancel(Resource):
    def put(self, parcel_id):
        """route for cancelling an order before delivery"""
        parcel = db.get_single_order(parcel_id)
        if parcel:
            db.update_order(parcel_id, 'cancelled')
            return {"message": "success", "new details": db.get_single_order(parcel_id)}
        return {"error": "parcel does not exist"}, 404


class Destination(Resource):
    @v1_order.expect(update_destination)
    def put(self, parcel_id):
        """route used to change the destination of a parcel delivery order"""
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        parcel = db.get_single_order(parcel_id)
        if parcel:

            data = DestinationParser.parser.parse_args()
            destination = data['destination']
            if len(destination) < 3 or destination == '':
                return {'error': 'please provide a valid destination'}, 400
            if not isinstance(destination, str):
                return {"error": "destination cannot be a number"}, 400
            db.update_destination(parcel_id, destination)
            return {"message": "success", "new details": db.get_single_order(parcel_id)}
        return {"error": "parcel does not exist"}, 404


v1_order.add_resource(Order, '/', strict_slashes=False)
v1_order.add_resource(Orders, '/<int:parcel_id>', strict_slashes=False)
v1_order.add_resource(Cancel, '/<int:parcel_id>/cancel', strict_slashes=False)
v1_order.add_resource(Destination, '/<int:parcel_id>/destination', strict_slashes=False)

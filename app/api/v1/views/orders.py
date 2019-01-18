from flask_restplus import Resource, Namespace, reqparse, fields
from flask import request
from app.api.utils.app_docs import v1_order, new_order, update_destination
from app.api.utils.parcel_validator import ParcelSchema, DestinationSchema, validator
from ..models.orders_model import OrdersModel
from ..models.user_model import UserModel
from marshmallow import post_load

db = OrdersModel()
user_db = UserModel()


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
        error_types = ['sender_name', 'receiver_name',
                       'receiver_contact', 'weight', 'pickup_location', 'destination']
        errors = validator(schema, error_types, data)
        if errors:
            return errors
        user = user_db.exists(data['sender_name'])
        if user:
            db.create_order(sender_name=data['sender_name'], receiver_name=data['receiver_name'], receiver_contact=data['receiver_contact'], weight=data['weight'],
                            pickup_location=data['pickup_location'],
                            destination=data['destination'])
            return {"success": "order submitted successfully",
                    "Order details": data}, 201
        return {"error": "please sign up to create an order"}, 400


class Orders(Resource):

    def get(self, parcel_id):
        """route to get a single parcel delivery order"""
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

            data = v1_order.payload
            schema = DestinationSchema()
            error_types = ['destination']
            errors = validator(schema, error_types, data)
            if errors:
                return errors
            destination = data['destination']

            db.update_destination(parcel_id, destination)
            return {"message": "success", "new details": db.get_single_order(parcel_id)}
        return {"error": "parcel does not exist"}, 404


v1_order.add_resource(Order, '/', strict_slashes=False)
v1_order.add_resource(Orders, '/<int:parcel_id>', strict_slashes=False)
v1_order.add_resource(Cancel, '/<int:parcel_id>/cancel', strict_slashes=False)
v1_order.add_resource(
    Destination, '/<int:parcel_id>/destination', strict_slashes=False)

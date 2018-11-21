from flask_restplus import Resource, Namespace, fields
from flask import request
from app.api.utils.parcel_validator import ParcelSchema
from ..models.orders_model import OrderModel
from marshmallow import post_load
from flask_jwt_extended import jwt_required, get_jwt_identity

v2_order = Namespace('parcels')
new_order = v2_order.model('Orders', {
    'sender_name': fields.String(description="John Doe"),
    'receiver_name': fields.String("Alfie kavaluku"),
    'receiver_contact': fields.String("alfie@gmail.com"),
    'weight': fields.Integer(10),
    'pickup_location': fields.String('kiambu'),
    'destination': fields.String("nairobi")
})


class Order(Resource):
    """ class that owns the routes to create and get all parcels"""

    @jwt_required
    @v2_order.expect(new_order)
    @post_load
    def post(self):
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        data = v2_order.payload
        schema = ParcelSchema()
        result = schema.load(data)
        errors = result.errors
        error_types = ['sender_name', 'receiver_name', 'receiver_contact', 'weight', 'pickup_location', 'destination']

        for e in error_types:
            if e in errors.keys():
                return {'message': errors[e][0]}, 400
        user_id = get_jwt_identity()
        if user_id:
            order = OrderModel(data['sender_name'], user_id, data['receiver_name'], data['receiver_contact'],
                               data['weight'], \
                               data['pickup_location'], \
                               data['destination'])
            order.create_order()
            return {"success": "order submitted successfully",
                    "Order details": data}, 201

        return {"message":"please login"}
v2_order.add_resource(Order, "", strict_slashes=False)

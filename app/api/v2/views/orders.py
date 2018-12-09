from flask_restplus import Resource, Namespace, reqparse, fields
from flask import request
from app.api.utils.parcel_validator import ParcelSchema, DestinationParser, LocationParser, StatusParser
from ..models.orders_model import OrderModel
from marshmallow import post_load
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.utils.mailgun import Mailgun
v2_order = Namespace('parcels')
new_order = v2_order.model('Orders', {
    'sender_name': fields.String(description="John Doe"),
    'receiver_name': fields.String("Alfie kavaluku"),
    'receiver_contact': fields.String("alfie@gmail.com"),
    'weight': fields.Integer(10),
    'pickup_location': fields.String('kiambu'),
    'destination': fields.String("nairobi")
})
update_destination = v2_order.model('order', {
    'destination': fields.String(description='destination')
})

location = v2_order.model('order', {
    'location': fields.String(description='location')
})
order_status = v2_order.model('order', {
    'order_status': fields.String(description='order_status')
})


class Order(Resource):
    """ class that owns the routes to create and get all parcels"""

    @jwt_required
    @v2_order.expect(new_order)
    @post_load
    def post(self):
        """route for creating a parcel delivery order"""
        if not request.is_json:
            return {"error ": "Missing user details or invalid input format"}, 400
        data = v2_order.payload
        schema = ParcelSchema()
        result = schema.load(data)
        errors = result.errors
        error_types = ['sender_name', 'receiver_name',
                       'receiver_contact', 'weight', 'pickup_location', 'destination']

        for error in error_types:
            if error in errors.keys():
                return {'message': {error: errors[error][0]}}, 400
        user_id = get_jwt_identity()
        if user_id:
            order = OrderModel(data['sender_name'], user_id, data['receiver_name'], data['receiver_contact'],
                               data['weight'], data['pickup_location'], data['destination'])
            order.create_order()
            return {"success": "order submitted successfully",
                    "order details": data}, 201

        return {"message": "please login"}

    @jwt_required
    def get(self):
        """method for getting all orders available in the database"""
        orders = OrderModel.get_all_orders()
        return orders, 200


class OrderById(Resource):
    @jwt_required
    def get(self, parcel_id):
        order = OrderModel.check_exists(parcel_id)
        if order:
            user_id = get_jwt_identity()
            parcel_owner = OrderModel.check_user(parcel_id)
            if user_id == parcel_owner:
                return OrderModel.get_single_order(parcel_id), 200
            return {"error": "you do not have the previledges to perform this action"}
        return {"message": "order does not exist"}, 404


class Destination(Resource):
    @jwt_required
    @v2_order.expect(update_destination)
    def put(self, parcel_id):
        """route used to change the destination of a parcel delivery order"""
        if not request.is_json:
            return {"error": "Missing user details or invalid input format"}, 400
        data = DestinationParser.parser.parse_args()
        destination = data['destination']

        if len(destination) < 3 or destination == '':
            return {'error': 'please provide a valid destination'}, 400

        if not isinstance(destination, str):
            return {"error": "destination cannot be a number"}, 400
        order = OrderModel.check_exists(parcel_id)
        if order:
            user_id = get_jwt_identity()
            parcel_owner = OrderModel.check_user(parcel_id)
            if user_id == parcel_owner:
                check_cancel = OrderModel.cancelled_or_delivered(parcel_id)
                if check_cancel:
                    OrderModel.update_destination(
                        parcel_id, destination, user_id)
                    return OrderModel.get_single_order(parcel_id)
                return {"message": "order is either delivered or already cancelled"}
            return {"error": "you do not have the previledges to perform this action"}
        return {"error": "parcel does not exist"}, 404


class Cancel(Resource):
    @jwt_required
    def put(self, parcel_id):
        """route for cancelling an order before delivery"""
        parcel = OrderModel.check_exists(parcel_id)

        if parcel:
            user_id = get_jwt_identity()
            parcel_owner = OrderModel.check_user(parcel_id)
            if user_id == parcel_owner:
                return OrderModel.cancel_order(parcel_id, user_id)
            return {"message": "you dont have the priviledges to perform this action"}
        return {"error": "parcel does not exist"}, 404


class ChangeLocation(Resource):
    @jwt_required
    @v2_order.expect(location)
    def put(self, parcel_id):
        """route used to change the destination of a parcel delivery order"""
        if not request.is_json:
            return {"error": "Missing user details or invalid input format"}, 400
        data = LocationParser.parser.parse_args()
        location = data['location']

        if len(location) < 3 or location == '':
            return {'error': 'please provide a valid location'}, 400

        if not isinstance(location, str):
            return {"error": "location cannot be a number"}, 400
        order = OrderModel.check_exists(parcel_id)
        if order:
            user_id = get_jwt_identity()
            parcel_owner = OrderModel.check_user(parcel_id)
            if user_id == parcel_owner:
                check_cancel = OrderModel.cancelled_or_delivered(parcel_id)
                if check_cancel:
                    if OrderModel.get_single_order(1)['current_location'] == location:
                        return {"message": "location is similar to the current location"}
                    OrderModel.change_location(parcel_id, location)
                    Mailgun.send_email(["benlegendj@gmail.com"], subject="change location",
                                       content="location has been change successfully")
                    return OrderModel.get_single_order(parcel_id)
                return {"message": "order is either delived or already canceled"}
            return {"message": "you dont have the priviledges to perform this action"}
        return {"error": "parcel does not exist"}, 404


class ChangeStatus(Resource):
    @jwt_required
    @v2_order.expect(order_status)
    def put(self, parcel_id):
        """route used to change the status of a parcel delivery order"""
        if not request.is_json:
            return {"error": "Missing user details or invalid input format"}, 400
        data = StatusParser.parser.parse_args()
        order_status = data['status']

        if len(order_status) < 3 or order_status == '':
            return {'error': 'please provide a valid order_status'}, 400

        if not isinstance(order_status, str):
            return {"error": "order_status cannot be a number"}, 400
        order = OrderModel.check_exists(parcel_id)
        if order:
            check_cancel = OrderModel.cancelled_or_delivered(parcel_id)
            if check_cancel:
                OrderModel.change_status(parcel_id, order_status)
                Mailgun.send_email(["benlegendj@gmail.com"], subject="change order status",
                                   content="status has been change successfully")
                return OrderModel.get_single_order(parcel_id)
            return {"message": "order is either delivered or already cancelled"}
        return {"error": "parcel does not exist"}, 404


v2_order.add_resource(Order, "", strict_slashes=False)
v2_order.add_resource(
    Destination, "/<int:parcel_id>/destination", strict_slashes=False)
v2_order.add_resource(Cancel, "/<int:parcel_id>/cancel", strict_slashes=False)
v2_order.add_resource(
    ChangeLocation, "/<int:parcel_id>/changelocation", strict_slashes=False)
v2_order.add_resource(
    ChangeStatus, "/<int:parcel_id>/status", strict_slashes=False)
v2_order.add_resource(OrderById, "/<int:parcel_id>", strict_slashes=False)

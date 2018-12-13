from app.api.utils.app_docs import new_order, update_destination, location, order_status, v2_order
from flask_restplus import Resource, Namespace, reqparse, fields
from flask import request
from app.api.utils.parcel_validator import ParcelSchema, validator, DestinationSchema, LocationSchema, StatusSchema
from ..models.orders_model import OrderModel
from marshmallow import post_load
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.utils.mailgun import Mailgun
from app.api.utils.admin import admin_required


class Order(Resource):
    """ class that owns the routes to create and get all parcels"""

    @jwt_required
    @v2_order.expect(new_order)
    @post_load
    def post(self):
        """route for creating a parcel delivery order"""
        if not request.json:
            return {"error ": "Missing user details or invalid input format"}, 400
        data = v2_order.payload
        schema = ParcelSchema()
        error_types = ['sender_name', 'receiver_name',
                       'receiver_contact', 'weight', 'pickup_location', 'destination']
        errors = validator(schema, error_types, data)
        if errors:
            return errors
        user_id = get_jwt_identity()
        if user_id:
            order = OrderModel(data['sender_name'], user_id, data['receiver_name'], data['receiver_contact'],
                               data['weight'], data['pickup_location'], data['destination'])
            order.create_order()
            return {"success": "order submitted successfully",
                    "order details": data}, 201

        return {"message": "please login"}

    @jwt_required
    @admin_required
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
        if not request.json:
            return {"error": "Missing user details or invalid input format"}, 400
        data = v2_order.payload
        schema = DestinationSchema()
        error_types = ['destination']
        errors = validator(schema, error_types, data)
        if errors:
            return errors
        destination = data['destination']

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
    @admin_required
    @v2_order.expect(location)
    def put(self, parcel_id):
        """route used to change the destination of a parcel delivery order"""
        if not request.json:
            return {"error": "Missing user details or invalid input format"}, 400
        data = v2_order.payload
        schema = LocationSchema()
        error_types = ['location']
        errors = validator(schema, error_types, data)
        if errors:
            return errors
        location = data['location']

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
    @admin_required
    @v2_order.expect(order_status)
    def put(self, parcel_id):
        """route used to change the status of a parcel delivery order"""
        if not request.json:
            return {"error": "Missing user details or invalid input format"}, 400
        data = StatusParser.parser.parse_args()
        data = v2_order.payload
        schema = StatusSchema()
        error_types = ['status']
        errors = validator(schema, error_types, data)
        if errors:
            return errors
        order_status = data['status']

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

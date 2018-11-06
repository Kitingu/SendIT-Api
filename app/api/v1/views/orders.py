from flask_restplus import Resource, Namespace, reqparse, fields
# from app.api.v1.models.orders_model import OrdersModel
from app.api.utils.parcel_validator import ParcelSchema
from ..models.orders_model import OrdersModel

db = OrdersModel()
v1_ns = Namespace('parcels')
new_order = v1_ns.model('Orders', {
    'sender_name': fields.String(description="John Doe"),
    'receiver_name': fields.String("Alfie kavaluku"),
    'receiver_contact': fields.String("alfie@gmail.com"),
    'weight': fields.Integer(10),
    'pickup_location': fields.String('kiambu'),
    'destination': fields.String("nairobi")
})


@v1_ns.route('/')
class Order(Resource):
    """ class that owns the routes to create and get all parcels"""

    def get(self):
        """ route that returns all the parcels in the database"""
        response = db.get_all_order()
        return response, 200

    @v1_ns.expect(new_order)
    def post(self):
        data = v1_ns.payload
        schema = ParcelSchema()
        schema_data = schema.load(data)
        errors = schema_data.errors
        error_types = ['sender_name', 'receiver_name', 'receiver_contact', 'weight', 'pickup_location', 'destination']
        for e in error_types:
            if e in errors.keys():
                return {'message': errors[e][0]}, 400
        db.create_order(data['sender_name'], data['receiver_name'], data['receiver_contact'], data['weight'], \
                        data['pickup_location'], \
                        data['destination'])
        return {"success": "order submitted successfully",
                "Order details": data}, 201


@v1_ns.route('/<int:parcel_id>')
class Orders(Resource):

    def get(self, parcel_id):
        response = db.get_single_order(parcel_id)
        if response:
            return {"message":response}, 200
        return {"error": "parcel order does not exist"}, 404

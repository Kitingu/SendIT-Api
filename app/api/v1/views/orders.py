from flask_restplus import Resource, Namespace, reqparse, fields
# from app.api.v1.models.orders_model import OrdersModel
from app.api.utils.parcel_validator import ParcelSchema
from ..models.orders_model import OrdersModel
from marshmallow import post_load

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
update_order = v1_ns.model('order', {
    'status': fields.String(description='cancel')
})


@v1_ns.route('/')
class Order(Resource):
    """ class that owns the routes to create and get all parcels"""

    def get(self):
        """ route that returns all the parcels in the database"""
        response = db.get_all_order()
        return response, 200

    @v1_ns.expect(new_order)
    @post_load
    def post(self):
        data = v1_ns.payload
        schema = ParcelSchema()
        result = schema.load(data)
        errors = result.errors
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
            return {"message": response}, 200
        return {"error": "parcel order does not exist"}, 404

    @v1_ns.expect(update_order)
    def put(self, parcel_id):
        parser = reqparse.RequestParser()
        parcel = db.get_single_order(parcel_id)
        if parcel:
            parser.add_argument('status',
                                type=str,
                                required=True,
                                help='input cancel or CANCEL to cancel the order')
            data = parser.parse_args()
            if data['status'] == 'CANCEL' or data['status'] == 'cancel':
                db.update_order(parcel_id, 'cancelled')
                return {"message": "success", "new details": db.get_single_order(parcel_id)}
            return {"error": "input cancel or CANCEL to cancel the order"}, 400

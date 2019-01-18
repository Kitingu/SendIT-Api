from flask_restplus import fields, Namespace

v2_order = Namespace('parcels')
v1_user = Namespace('users')
v1_order = Namespace('parcels')
v2_user = Namespace("auth")

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


new_user = v2_user.model("Users", {"email": fields.String("email@example.com"),
                                   "username": fields.String("test_user"),
                                   "password": fields.String("test_pass"),
                                   "confirm_password": fields.String("test_pass")
                                   })

user_login = v2_user.model("Login", {"email": fields.String("email@example.com"),
                                     "password": fields.String("test_pass")})

from flask_restplus import Resource, Namespace, reqparse, fields
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request
from app.api.utils.parcel_validator import UserSchema, LoginParser
from ..models.user_model import UserModel
from ..models.orders_model import OrdersModel
from marshmallow import post_load
from instance.config import Config
import datetime, jwt

user_db = UserModel()
order_db = OrdersModel()
v1_user = Namespace('users')
new_user = v1_user.model('Users', {'email': fields.String('email@example.com'),
                                   'username': fields.String('test_user'),
                                   'password': fields.String('test_pass'),
                                   'confirm_password': fields.String('test_pass')

                                   })

user_login = v1_user.model('Login', {'email': fields.String('email@example.com'),
                                     'password': fields.String('test_pass')})


class User(Resource):
    @v1_user.expect(new_user)
    @post_load()
    def post(self):
        """route for user registration"""
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        data = v1_user.payload
        schema = UserSchema()
        result = schema.load(data)
        errors = result.errors
        error_types = ['username', 'email', 'password']
        for e in error_types:
            if e in errors.keys():
                return {'message': errors[e][0]}, 400
        hashed_pass = generate_password_hash(data['password'])
        new_user = user_db.get_single_user(data['email'])
        if new_user:
            return "user with email: {} already exists".format(data["email"]), 409
        if check_password_hash(hashed_pass, data['confirm_password']):
            user_db.save(data['email'], data['username'], hashed_pass)
            return {"message": "User registered successfully"}, 201
        return {"error": "passwords do not match"}, 401

    def get(self):
        """route for getting all users"""
        return user_db.get_all_users()




class Login(Resource):
    @v1_user.expect(user_login)
    def post(self):
        """route that allows users  to log in"""
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        data = LoginParser.parser.parse_args()
        email = str(data['email'])
        password = str(data['password'])

        user = user_db.get_single_user(email)
        if user:
            if check_password_hash(user_db.db[email]['password'], password):
                access_token = jwt.encode(
                    {"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                    Config.SECRET_KEY)
                return {"access_token": access_token.decode('utf-8')}, 200
            return {"msg": "Invalid email or password"}, 401

        return "user does not exist", 400


class UserParcels(Resource):
    """ route for getting orders made by a specific user"""

    def get(self, user_id):
        """route for getting order by specific user"""
        resp = order_db.get_by_specific_user(user_id)
        if resp:
            return order_db.get_by_specific_user(user_id)
        return {"message": "user does not exist"}, 404


v1_user.add_resource(User, '', strict_slashes=False)
v1_user.add_resource(Login, '/login', strict_slashes=False)
v1_user.add_resource(UserParcels, '/<user_id>/parcels', strict_slashes=False)

from flask_restplus import Resource, Namespace, fields
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request
from app.api.utils.parcel_validator import UserSchema
from ..models.user_model import UserModel
from marshmallow import post_load

v2_user = Namespace('users')
new_user = v2_user.model('Users', {'email': fields.String('email@example.com'),
                                   'username': fields.String('test_user'),
                                   'password': fields.String('test_pass'),
                                   'confirm_password': fields.String('test_pass')

                                   })

user_login = v2_user.model('Login', {'email': fields.String('email@example.com'),
                                     'password': fields.String('test_pass')})


class User(Resource):
    @v2_user.expect(new_user)
    @post_load()
    def post(self):
        """route for user registration"""
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        data = v2_user.payload
        schema = UserSchema()
        result = schema.load(data)
        errors = result.errors
        error_types = ['username', 'email', 'password']
        for e in error_types:
            if e in errors.keys():
                return {'message': errors[e][0]}, 400
        hashed_pass = generate_password_hash(data['password'])
        # new_user = UserModel.get_single_user(data['email'])
        new_user = UserModel.exists(data['username'])
        if new_user:
            return "user with username: {} already exists".format(data["email"]), 409
        if check_password_hash(hashed_pass, data['confirm_password']):
            user = UserModel(data['email'], data['username'], hashed_pass)
            user.create_user()
            return {"message": "User registered successfully"}, 201
        return {"error": "passwords do not match"}, 401


v2_user.add_resource(User, '', strict_slashes=False)

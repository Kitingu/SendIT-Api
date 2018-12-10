from flask_restplus import Resource, Namespace, fields, reqparse
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
from app.api.utils.parcel_validator import UserSchema, LoginParser
from ..models.user_model import UserModel
from app.api.v2.views import blacklist
from marshmallow import post_load
from app.api.utils.admin import admin_required

v2_user = Namespace("auth")
new_user = v2_user.model("Users", {"email": fields.String("email@example.com"),
                                   "username": fields.String("test_user"),
                                   "password": fields.String("test_pass"),
                                   "confirm_password": fields.String("test_pass")
                                   })

user_login = v2_user.model("Login", {"email": fields.String("email@example.com"),
                                     "password": fields.String("test_pass")})


class User(Resource):
    @v2_user.expect(new_user)
    @post_load()
    def post(self):
        """route for user registration"""
        if not request.is_json:
            return {"message": "Missing user details or invalid input format"}, 400
        data = v2_user.payload
        schema = UserSchema()
        result = schema.load(data)
        errors = result.errors
        error_types = ["username", "email", "password"]

        for error in error_types:
            if error in errors.keys():
                return {"message": errors[error][0]}, 400
        hashed_pass = generate_password_hash(data["password"])
        new_user = UserModel.exists(data["username"])
        mailexists = UserModel.mailexists(data["email"])

        if new_user:
            return "user with username: {} already exists".format(data["username"]), 409
        if mailexists:
            return "user with email: {} already exists".format(data["email"]), 409
        if check_password_hash(hashed_pass, data["confirm_password"]):
            user = UserModel(data["email"], data["username"], hashed_pass)
            user.create_user()
            return {"message": "User registered successfully"}, 201
        return {"error": "passwords do not match"}, 401


class Login(Resource):
    @v2_user.expect(user_login)
    def post(self):
        """"log in users using email and password"""
        if not request.is_json:
            return {"message": "Missing user details or invalid input format"}, 400
        data = LoginParser.parser.parse_args()
        email = str(data['email'])
        password = str(data['password'])

        user = [user for user in UserModel.get_all_users()
                if user['email'] == email]
        if user:
            if check_password_hash(user[0]['password'], password):
                access_token = create_access_token(identity=user[0]['user_id'])
                return {"access_token": access_token}, 200
            return {"error": "Invalid email or password"}, 401

        return "user does not exist", 400


class Logout(Resource):
    """logout users"""

    @v2_user.doc(security="apikey")
    @jwt_required
    def post(self):
        """Log out a given user by blacklisting user's token"""
        jti = get_raw_jwt()["jti"]
        blacklist.add(jti)
        return ({'message': "Successfully logged out"}), 200


class GetUsers(Resource):
    @jwt_required
    @admin_required
    def get(self):
        return UserModel.get_all_users()


class GetSingleUser(Resource):
    @jwt_required
    @admin_required
    def get(self, username):
        return UserModel.get_single_user(username)


v2_user.add_resource(User, "/signup", strict_slashes=False)
v2_user.add_resource(Login, "/login", strict_slashes=False)
v2_user.add_resource(Logout, "/logout", strict_slashes=False)
v2_user.add_resource(GetUsers, "", strict_slashes=False)
v2_user.add_resource(GetSingleUser, "/<string:username>", strict_slashes=False)

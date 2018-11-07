from flask_restplus import Resource, Namespace, reqparse, fields
from werkzeug.security import check_password_hash, generate_password_hash
from app.api.utils.parcel_validator import UserSchema
from ..models.user_model import UserModel
from marshmallow import post_load

db = UserModel()
v1_user = Namespace('users')
new_user = v1_user.model('Users', {'email': fields.String('email@example.com'),
                                    'username': fields.String('test_user'),
                                    'password': fields.String('test_pass'),
                                    'confirm_password': fields.String('test_pass')

                                    })
@v1_user.route('/')
class User(Resource):
    @v1_user.expect(new_user)
    @post_load()
    def post(self):
        data = v1_user.payload
        schema = UserSchema()
        result = schema.load(data)
        errors = result.errors
        error_types = ['username','email','password']
        for e in error_types:
            if e in errors.keys():
                return {'message': errors[e][0]}, 400
        hashed_pass = generate_password_hash(data['password'])
        new_user = db.get_single_user(data['email'])
        if new_user:
            return "user with email: {} already exists".format(data["email"]),409
        if check_password_hash(hashed_pass, data['confirm_password']):
            db.save(data['email'], data['username'], hashed_pass)
            return {"message":"User registered successfully"}, 201
        return {"error":"passwords do not match"}, 401



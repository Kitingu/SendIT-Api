from flask_jwt_extended import get_jwt_identity
from functools import wraps
from app.api.v2.models.user_model import UserModel


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        admin = UserModel.get_user_by_id(get_jwt_identity())
        if admin != True:
            return {'message': 'you dont have the privilege to perform this task consult administrator'}, 401
        return f(*args, **kwargs)
    return wrapper

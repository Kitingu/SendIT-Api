from flask import jsonify, request, make_response
from functools import wraps
import jwt

from instance.config import Config


def token_required(f):
    """Checks for authenticated users with valid token in the header"""

    @wraps(f)
    def decorated(*args, **kwargs):
        """function to that to make a jwt_token_required decorator"""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({"message": "Please Sign up and Login"}), 401)

        try:
            data = str(jwt.decode(token, Config.SECRET))
        except():
            return make_response(jsonify({"message": "Please, provide a valid token."}), 401)
        return f(*args, **kwargs)

    return decorated

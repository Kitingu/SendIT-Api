from flask import jsonify, request, make_response
from functools import wraps
import jwt

from instance.config import Config


def token_required(f):
    """Checks for authenticated users with valid token in the header"""

    @wraps(f)
    def decorated(*args, **kwargs):
        """validate token provided"""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({"txt": "Please Register and Login"}), 401)

        try:
            data = str(jwt.decode(token, Config.SECRET))
        except():
            return make_response(jsonify({"txt": "Please, provide a valid token."}), 401)
        return f(*args, **kwargs)

    return decorated

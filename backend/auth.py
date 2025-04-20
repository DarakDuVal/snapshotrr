from functools import wraps
from flask import request, jsonify
from db import verify_user

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not verify_user(auth.username, auth.password):
            return jsonify({"error": "Unauthorized"}), 401, {'WWW-Authenticate': 'Basic realm="Login required"'}
        return f(*args, **kwargs)
    return decorated

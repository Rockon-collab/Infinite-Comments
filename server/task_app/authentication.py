from functools import wraps
from flask import session, jsonify

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             return jsonify({"error": "Authentication required."}), 401
#         return f(*args, **kwargs)
#     return decorated_function
from flask import request
import jwt
from datetime import datetime, timedelta
from . import app

def create_jwt_token(user_id, username, remember_me):
    expiration_time = timedelta(days=30) if remember_me else timedelta(hours=1)
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + expiration_time,  # Token expiration
        "iat": datetime.utcnow()  # Issued at
    }
    secret_key = app.config['SECRET_KEY']  # Ensure you have a SECRET_KEY set in your app configuration
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_jwt_token(token):
    try:
        secret_key = app.config['SECRET_KEY']
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


def get_user_from_token(token):
    try:
        secret_key = app.config['SECRET_KEY']
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Remove "Bearer " prefix if present
            token = token.split(" ")[1] if " " in token else token
            payload = decode_jwt_token(token)
            if "error" in payload:
                return jsonify({"error": payload["error"]}), 401

            # Attach user info to `g`
        except Exception as e:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function

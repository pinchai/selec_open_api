from functools import wraps
from itsdangerous import SignatureExpired, BadSignature
from flask import request, jsonify
from config import query
from routes.setting import get_serializer


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        serializer = get_serializer()
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "").strip()

        if not token:
            return jsonify({"status": "error", "message": "Missing token"}), 401

        try:
            data = serializer.loads(token, max_age=60 * 60 * 24 * 90)
            user_id = data.get("user_id")
        except SignatureExpired:
            return jsonify({"status": "error", "message": "Token expired"}), 401
        except BadSignature:
            return jsonify({"status": "error", "message": "Invalid token"}), 401

        # Check if user exists
        user = query("SELECT id, email, created_at FROM user WHERE id = ?", (user_id,), one=True)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        # Attach user to Flask global `g` so routes can access it
        # g.current_user = dict(user)

        return f(*args, **kwargs)

    return decorated


def get_user_id_from_token():
    serializer = get_serializer()
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    if not token:
        return 'token not found !'

    try:
        data = serializer.loads(token, max_age=60 * 60 * 24 * 90)
        return data.get("user_id")
    except (SignatureExpired, BadSignature):
        return 'Invalid or expired token !'

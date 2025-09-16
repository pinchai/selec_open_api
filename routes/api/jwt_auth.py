from flask import request, jsonify
from werkzeug.security import check_password_hash

from config import query
from app import app, create_access_token, jwt_required, get_jwt_identity, jwt
from flask_jwt_extended import get_jwt
from datetime import timedelta


# Simple in-memory blocklist (replace with DB/Redis in production)
BLOCKLIST = set()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST   # True means revoked → request blocked


@app.post('/api/login')
def jwt_login():
    """
    Login
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "pinchai.pc@gmail.com"
            password:
              type: string
              example: "12345678"
    responses:
      200:
        description: login successful
        schema:
          type: object
          properties:
            status: { type: string, example: success }
            data:
              type: object
              properties:
                token: { type: string }
      400:
        description: Validation error
    """
    email = request.json.get("email", "").strip().lower()
    password = request.json.get("password", "").strip()

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and Password are required."}), 400

    user = query("SELECT * FROM user WHERE email = ?", (email,), one=True)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"status": "error", "message": "Invalid password."}), 401

    if user["verify"] == 0:
        return jsonify({"status": "error", "message": "Email not verified."}), 403

    claims = {
        "email": user['email'],
    }
    user_id = str(user['id'])
    token = create_access_token(
        identity=user_id,
        additional_claims=claims,
        expires_delta=timedelta(hours=24)
    )
    return jsonify(access_token=token), 200


@app.post("/api/logout")
@jwt_required()
def jwt_logout():
    """
    Logout (invalidate current token)
    ---
    tags:
      - Auth
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: "Bearer <access token>"
    responses:
      200:
        description: logout successful
    """
    jti = get_jwt()["jti"]  # unique identifier for this token
    BLOCKLIST.add(jti)      # mark as revoked
    return jsonify({"status": "success", "message": "Logged out successfully."}), 200


@app.get("/api/me")
@jwt_required()
def me():
    """
    Current user information
    ---
    tags:
      - Auth
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: "Bearer access token"
    responses:
      200:
        description: successful
    """
    user_id = get_jwt_identity()
    claims = get_jwt()
    return {
        "user": {
            "user_id": user_id,
            "data": claims,
        }
    }




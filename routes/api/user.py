from app import app
from flask import request, jsonify

from config import query
from routes.setting import get_serializer


@app.post("/api/v1/user/get-me")
def get_me():
    """
    get user information (JSON)
    ---
    tags:
      - User   # 👈 this will group it under "Math"
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: string
          properties:
            token:
              type: string
              example: eyJ1c2VyX2lkIjoxfQ.aLbhnA.6nH89Ajo1SFmnaLaZ6pBnMwomNs
    responses:
      200:
        description: OK
        # schema:
        #   type: object
        #   properties:
        #     result:
        #       type: integer
    """
    serializer = get_serializer()
    data = request.get_json()
    token = data.get("token")
    user_id = serializer.loads(token, max_age=60 * 60 * 24 * 90)["user_id"]
    user = query("SELECT email FROM user WHERE id = ?", (user_id,), one=True)
    if not user:
        return {
                   "status": "error",
                   "message": "User not found"
               }, 200
    else:
        return {
            "status": "success",
            "data": dict(user)
        }, 200

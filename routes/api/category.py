from app import app
from flask import request, jsonify
from config import query, execute
from routes.api.auth import token_required, get_user_id_from_token


@app.post("/api/v1/category/lists")
@token_required
def get_category_lists():
    """
    Get all category list (JSON)
    ---
    tags:
      - Category
    consumes:
      - application/json
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: "Bearer access token"
    responses:
      200:
        description: Category list
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: array
              items:
                type: object
                properties:
                  id: { type: integer, example: 1 }
                  name: { type: string, example: "Electronics" }
                  image: { type: string, example: "electronics.jpg" }
                  user_id: { type: integer, example: 1 }
    """
    user_id = get_user_id_from_token()
    try:
        rows = query("SELECT * FROM category WHERE user_id = ?", (user_id,), one=False)
        data = [dict(r) for r in rows] if rows else []
        return {"status": "success", "data": data}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@app.post("/api/v1/category/create")
@token_required
def create_category_api():
    """
    Create a new category
    ---
    tags:
      - Category
    consumes:
      - application/json
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: "Bearer access token"
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: "Drinks"
            image:
              type: string
              example: "drink.jpg"
    responses:
      200:
        description: Category created
        schema:
          type: object
          properties:
            status: { type: string, example: success }
            data:
              type: object
              properties:
                id: { type: integer }
                name: { type: string }
                image: { type: string }
                user_id: { type: integer }
      400:
        description: Validation error
    """
    data = request.get_json() or {}
    name = (data.get("name"))
    image = (data.get("image") or "")
    # assert False, name
    if not name:
        return {"status": "error", "message": "Category name is required"}, 400

    user_id = get_user_id_from_token()

    try:
        execute(
            "INSERT INTO category (name, image, user_id) VALUES (?, ?, ?)",
            (name, image, user_id)
        )
        new_cat = query("SELECT * FROM category WHERE rowid = last_insert_rowid()", one=True)
        return {"status": "success", "data": dict(new_cat)}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

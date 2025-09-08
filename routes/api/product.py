from app import app
from config import query, execute
from routes.api.auth import token_required, get_user_id_from_token


@app.post("/api/v1/product/lists")
@token_required
def get_product_lists():
    """
    Get all product list (JSON)
    ---
    tags:
      - Product
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
        description: Product list
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
                  category_id: { type: integer, example: 1 }
                  category_name: { type: string, example: "Drink" }
                  name: { type: string, example: "coca" }
                  cost: { type: decimal, example: "0.25" }
                  price: { type: decimal, example: "0.50" }
                  image: { type: string, example: 265c3976704a4d3fa81379a400c4f872.jpeg }
                  user_id: { type: integer, example: 1 }
    """
    user_id = get_user_id_from_token()
    try:
        rows = query(
            """
            SELECT p.*, c.name AS category_name
            FROM product p
            JOIN category c ON p.category_id = c.id
            WHERE p.user_id = ?
            ORDER BY p.id DESC
            """,
            (user_id,),
            one=False,
        )
        data = [dict(r) for r in rows] if rows else []
        return {"status": "success", "data": data}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

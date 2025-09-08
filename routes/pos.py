from app import app
from flask import render_template, session, jsonify, request
from helpers.main import login_required
from config import execute


@app.get('/pos')
@login_required
def pos():
    return render_template('POS/pos.html')


@app.get("/pos/get-data")
@login_required
def get_data():
    from routes.cateogory import getList
    from routes.product import getList as getProductList
    user_id = session.get("user_id", "")
    category_list = getList(user_id)
    product_list = getProductList(user_id)
    category = [dict(r) for r in category_list] if category_list else []
    product = [dict(r) for r in product_list] if product_list else []
    return {
        'category': category,
        'product': product,
    }


@app.post("/pos/create-sale")
@login_required
def create_sale():
    from datetime import datetime
    from config import get_db
    now = datetime.now()
    user_id = session.get("user_id", "")
    data = request.get_json()
    sale_list = data.get('selected_product')
    total_amount = data.get('total_amount')
    received_amount = data.get('received_amount')

    get_db().execute('begin transaction;')
    sale_id = execute(
        """
        INSERT INTO sale_order (order_date_time, total, paid, user_id)
        VALUES (?, ?, ?, ?)
        """,
        (
            now.strftime("%Y-%m-%d %H:%M:%S"),
            float(total_amount),
            float(received_amount),
            user_id
        ),
        commit=False
    )
    for sale in sale_list:
        product_id = sale.get('id')
        quantity = sale.get('qty')
        cost = 0
        price = sale.get('price')
        execute(
            """
            INSERT INTO sale_order_item (order_id, product_id, qty, cost, price)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                sale_id,
                int(product_id),
                int(quantity),
                float(cost),
                float(price),
            ),
            commit=False
        )
    get_db().execute('commit')

    return jsonify(
        {
            "status": "success",
            "sale_id": sale_id,
        }
    ), 200

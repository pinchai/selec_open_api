from app import app
from flask import render_template, session, request
from helpers.main import login_required
from config import query, execute


@app.get("/admin/sale-list")
@login_required
def sale_list():
    user_id = session.get("user_id", "")
    sale = query(
        """
        SELECT
            sale_order.*,
            user.email as user_email
        FROM
            sale_order
        INNER JOIN user on user.id = sale_order.user_id
        WHERE user_id = ?
        """,
        (user_id,),
        one=False
    )
    return render_template(
        "admin/sale/sale.html",
        module='sale_order_list',
        sale=sale,
    )


@app.get("/admin/sale-list-detail")
@login_required
def sale_list_detail():
    user_id = session.get("user_id", "")
    sale_id = request.args.get('sale_id', '')
    sale = query('SELECT * FROM sale_order WHERE id = ?', (sale_id,), one=True)
    sale_item = query('SELECT soi.*, p.name FROM sale_order_item soi JOIN product p ON soi.product_id = p.id WHERE soi.order_id = ?', (sale_id,), one=False)
    return render_template(
        "admin/sale/detail.html",
        module='sale_order_list',
        sale=sale,
        sale_item=sale_item
    )



def getList(user_id):
    return query("SELECT * FROM category WHERE user_id = ?", (user_id,), one=False)

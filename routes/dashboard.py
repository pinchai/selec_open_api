from flask import render_template, session
from helpers.main import login_required
from config import *


@app.get("/admin/dashboard")
@login_required
def admin():
    user_id = session.get("user_id", "")
    category = query("SELECT COUNT(*) FROM category where user_id = ?", (user_id,), one=True)
    product = query("SELECT COUNT(*) FROM product where user_id = ?", (user_id,), one=True)
    sale_order = query("SELECT COUNT(*) FROM sale_order where user_id = ?", (user_id,), one=True)
    # assert False, pprint(session)
    return render_template(
        "admin/dashboard.html",
        module='dashboard',
        category_count=category[0],
        product_count=product[0],
        sale_order_count=sale_order[0],
        transaction_count=0,
    )

from app import app
from flask import render_template, session, jsonify, request, redirect, url_for, flash, current_app

from helpers.image_upload import save_image, remove_file_if_exists
from helpers.main import login_required
from config import query, execute
import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename


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

#
# @app.post("/pos/create-sale")
# @login_required
# def create_sale():
#     user_id = session.get("user_id", "")
#     name = (request.form.get("name") or "").strip()
#     category_id = (request.form.get("category_id") or "").strip()
#     cost = (request.form.get("cost") or "").strip() or None
#     price = (request.form.get("price") or "").strip() or None
#     stock = (request.form.get("current_stock") or "0").strip()
#     description = (request.form.get("description") or "").strip()
#
#     if not name:
#         flash("Product name is required.", 'danger')
#         return redirect(url_for("product"))
#     if not category_id.isdigit():
#         flash("Valid category is required.", 'danger')
#         return redirect(url_for("index_product"))
#
#     # Handle image upload (same style as category create)
#     file = request.files.get("image")
#     image_filename = None
#
#     if file and file.filename:
#         allowed_ext = {"png", "jpg", "jpeg", "gif", "webp"}
#         ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
#         if ext not in allowed_ext:
#             flash("Invalid image type. Allowed: png, jpg, jpeg, gif, webp", 'danger')
#             return redirect(url_for("index_product"))
#
#         upload_root = current_app.config.get(
#             "UPLOAD_FOLDER",
#             os.path.join(current_app.root_path, "static", "uploads", "product"),
#         )
#         Path(upload_root).mkdir(parents=True, exist_ok=True)
#
#         unique_name = f"{uuid.uuid4().hex}.{ext}"
#         safe_name = secure_filename(unique_name)
#         save_path = os.path.join(upload_root, safe_name)
#         try:
#             file.save(save_path)
#             image_filename = safe_name
#         except Exception as e:
#             current_app.logger.exception("Image upload failed: %s", e)
#             flash("Failed to upload image. Please try again.", 'danger')
#             return redirect(url_for("index_product"))
#
#     execute(
#         """
#         INSERT INTO product (name, category_id, cost, price, image, current_stock, description, user_id)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             name,
#             int(category_id),
#             cost,
#             price,
#             image_filename,
#             int(stock or 0),
#             description,
#             user_id,
#         ),
#     )
#
#     flash("Product created successfully.", 'success')
#     return redirect(url_for("product"))

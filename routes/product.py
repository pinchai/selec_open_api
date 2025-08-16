from app import app
from flask import render_template, session, request, redirect, url_for, flash, current_app

from helpers.image_upload import save_image, remove_file_if_exists
from helpers.main import login_required
from config import query, execute
import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename


@app.get("/admin/product")
@login_required
def product():
    user_id = session.get("user_id", "")
    products = query(
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

    return render_template(
        "admin/product/product.html",
        module="product",
        products=products
    )


@app.get("/admin/index_product")
@login_required
def index_product():
    from routes.cateogory import getList
    user_id = session.get("user_id", "")
    return render_template(
        "admin/product/create.html",
        module="product",
        categories=getList(user_id)
    )


@app.post("/admin/create_product")
@login_required
def create_product():
    user_id = session.get("user_id", "")
    name = (request.form.get("name") or "").strip()
    category_id = (request.form.get("category_id") or "").strip()
    cost = (request.form.get("cost") or "").strip() or None
    price = (request.form.get("price") or "").strip() or None
    stock = (request.form.get("current_stock") or "0").strip()
    description = (request.form.get("description") or "").strip()

    if not name:
        flash("Product name is required.", 'danger')
        return redirect(url_for("product"))
    if not category_id.isdigit():
        flash("Valid category is required.", 'danger')
        return redirect(url_for("index_product"))

    # Handle image upload (same style as category create)
    file = request.files.get("image")
    image_filename = None

    if file and file.filename:
        allowed_ext = {"png", "jpg", "jpeg", "gif", "webp"}
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in allowed_ext:
            flash("Invalid image type. Allowed: png, jpg, jpeg, gif, webp", 'danger')
            return redirect(url_for("index_product"))

        upload_root = current_app.config.get(
            "UPLOAD_FOLDER",
            os.path.join(current_app.root_path, "static", "uploads", "product"),
        )
        Path(upload_root).mkdir(parents=True, exist_ok=True)

        unique_name = f"{uuid.uuid4().hex}.{ext}"
        safe_name = secure_filename(unique_name)
        save_path = os.path.join(upload_root, safe_name)
        try:
            file.save(save_path)
            image_filename = safe_name
        except Exception as e:
            current_app.logger.exception("Image upload failed: %s", e)
            flash("Failed to upload image. Please try again.", 'danger')
            return redirect(url_for("index_product"))

    execute(
        """
        INSERT INTO product (name, category_id, cost, price, image, current_stock, description, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            int(category_id),
            cost,
            price,
            image_filename,
            int(stock or 0),
            description,
            user_id,
        ),
    )

    flash("Product created successfully.", 'success')
    return redirect(url_for("product"))


@app.get("/admin/index_edit_product")
@login_required
def index_edit_product():
    product_id = int(request.args.get("id")) if request.args.get("id") else 0
    if not product_id:
        flash("Product ID is required.", 'danger')
        return redirect(url_for("product"))

    product = query("SELECT * FROM product WHERE id = ?", (product_id,), one=True)
    if not product:
        flash("Product not found.", 'danger')
        return redirect(url_for("product"))

    user_id = session.get("user_id", "")
    categories = query("SELECT * FROM category WHERE user_id = ?", (user_id,), one=False)

    return render_template(
        "admin/product/edit.html",
        product=product,
        categories=categories,
        module="product",
    )


@app.post("/admin/edit_product")
@login_required
def edit_product():
    user_id = session.get("user_id", "")

    product_id = (request.form.get("id") or "").strip()
    name = (request.form.get("name") or "").strip()
    category_id = (request.form.get("category_id") or "").strip()
    cost = (request.form.get("cost") or "").strip() or None
    price = (request.form.get("price") or "").strip() or None
    stock = (request.form.get("current_stock") or "0").strip()
    description = (request.form.get("description") or "").strip()

    if not product_id.isdigit():
        flash("Invalid product ID.", 'danger')
        return redirect(url_for("product"))
    if not name:
        flash("Product name is required.", 'danger')
        return redirect(url_for("product"))
    if not category_id.isdigit():
        flash("Valid category is required.", 'danger')
        return redirect(url_for("index_edit_product") + f"?id={product_id}")

    # Ensure the product belongs to the user
    existing = query(
        "SELECT * FROM product WHERE id = ? AND user_id = ?",
        (product_id, user_id),
        one=True,
    )
    if not existing:
        flash("Product not found.", 'danger')
        return redirect(url_for("product"))

    new_image_name = existing["image"]
    file = request.files.get("image")

    if file and file.filename:
        try:
            saved_name = save_image(file_storage=file, folder="product")  # save new → then remove old after success
            if existing["image"] and existing["image"] != saved_name:
                remove_file_if_exists(filename=existing["image"], folder='product')
            new_image_name = saved_name
        except ValueError as ve:
            flash(str(ve), 'danger')
            return redirect(url_for("index_edit_product") + f"?id={product_id}")
        except Exception as e:
            current_app.logger.exception("Image upload failed: %s", e)
            flash("Failed to upload image. Please try again.", 'danger')
            return redirect(url_for("index_edit_product") + f"?id={product_id}")

    execute(
        """
        UPDATE product
        SET name = ?, category_id = ?, cost = ?, price = ?, image = ?, current_stock = ?, description = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            name,
            int(category_id),
            cost,
            price,
            new_image_name,
            int(stock or 0),
            description,
            int(product_id),
            user_id,
        ),
    )

    flash("Product updated successfully.", 'success')
    return redirect(url_for("product"))


@app.get("/admin/delete_product")
@login_required
def delete_product():
    user_id = session.get("user_id", "")
    product_id = request.args.get("id", "")

    if not product_id:
        flash("Product ID is required.", "error")
        return redirect(url_for("product"))

    execute("DELETE FROM product WHERE id = ? AND user_id = ?", (product_id, user_id))
    flash("Product deleted successfully.", "info")
    return redirect(url_for("product"))


def getList(user_id):
    return query(
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

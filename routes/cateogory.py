from app import app
from flask import render_template, session, request, redirect, url_for, flash, current_app
from helpers.main import login_required
from config import query, execute
import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename


@app.get("/admin/category")
@login_required
def category():
    user_id = session.get("user_id", "")
    categories = query("SELECT * FROM category WHERE user_id = ?", (user_id,), one=False)
    return render_template(
        "admin/category/category.html",
        module='category',
        category=categories,
    )


@app.get("/admin/index_category")
@login_required
def index_category():
    return render_template(
        "admin/category/create.html",
        module='category',
    )


@app.post("/admin/create_category")
@login_required
def create_category():
    user_id = session.get("user_id", "")
    name = request.form.get("name", "").strip()

    if not name:
        flash("Category name is required.")
        return redirect(url_for("category"))

    file = request.files.get("image")
    image_filename = None

    if file and file.filename:
        allowed_ext = {"png", "jpg", "jpeg", "gif", "webp"}
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in allowed_ext:
            flash("Invalid image type. Allowed: png, jpg, jpeg, gif, webp")
            return redirect(url_for("category"))

        upload_root = current_app.config.get(
            "UPLOAD_FOLDER",
            os.path.join(current_app.root_path, "static", "uploads", "category")
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
            flash("Failed to upload image. Please try again.")
            return redirect(url_for("category"))

    execute(
        "INSERT INTO category (name, image, user_id) VALUES (?, ?, ?)",
        (name, image_filename, user_id)
    )
    flash("Category created successfully.")
    return redirect(url_for("category"))


@app.post("/admin/edit_category")
@login_required
def edit_category():
    user_id = session.get("user_id", "")
    category_id = request.form.get("id", "")
    name = request.form.get("name", "").strip()
    image = request.form.get("image", "").strip() or None

    if not category_id or not name:
        flash("Category ID and name are required.")
        return redirect(url_for("category"))

    execute(
        "UPDATE category SET name = ?, image = ? WHERE id = ? AND user_id = ?",
        (name, image, category_id, user_id)
    )
    flash("Category updated successfully.")
    return redirect(url_for("category"))


@app.get("/admin/delete_category")
@login_required
def delete_category():
    user_id = session.get("user_id", "")
    category_id = request.args.get("id", "")

    if not category_id:
        flash("Category ID is required.")
        return redirect(url_for("category"))

    execute("DELETE FROM category WHERE id = ? AND user_id = ?", (category_id, user_id))
    flash("Category deleted successfully.")
    return redirect(url_for("category"))

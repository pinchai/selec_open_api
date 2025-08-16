import os
import uuid
from pathlib import Path

from flask import current_app
from werkzeug.utils import secure_filename


def get_upload_root(folder: str = "category"):
    return current_app.config.get(
        "UPLOAD_FOLDER",
        os.path.join(current_app.root_path, "static", "uploads", folder),
    )


def remove_file_if_exists(filename: str, folder: str = "category"):
    if not filename:
        return
    path = os.path.join(get_upload_root(folder), filename)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        current_app.logger.warning("Failed to remove file %s: %s", path, e)

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

def save_image(file_storage, folder: str = "category"):
    # returns safe filename (str) or raises ValueError on invalid type
    if not file_storage or not file_storage.filename:
        return None
    ext = file_storage.filename.rsplit(".", 1)[-1].lower() if "." in file_storage.filename else ""
    if ext not in ALLOWED_EXT:
        raise ValueError("Invalid image type. Allowed: png, jpg, jpeg, gif, webp")

    Path(get_upload_root(folder)).mkdir(parents=True, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    safe_name = secure_filename(unique_name)
    save_path = os.path.join(get_upload_root(folder), safe_name)
    file_storage.save(save_path)
    return safe_name

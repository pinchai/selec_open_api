from app import app
from flask import render_template, session
from helpers.main import login_required


@app.get("/admin/api_doc")
@login_required
def api_doc():
    user_id = session.get("user_id", "")
    return render_template(
        "admin/api_doc/api_doc.html",
        module='api_doc',
    )

from datetime import datetime, timedelta

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature, BadTimeSignature

from app import app
from flask import render_template, session, current_app, jsonify, redirect, url_for
from helpers.main import login_required
from config import query, execute


@app.get("/admin/setting")
@login_required
def setting():
    user_id = session.get("user_id", "")
    setting = query("SELECT * FROM user WHERE id = ?", (user_id,), one=True)
    # assert False, verify_token(setting[5])
    return render_template(
        "admin/setting/setting.html",
        module='setting',
        setting=setting,
        token_status=verify_token(setting[5])
    )


@app.get("/admin/setting/generate_token")
@login_required
def generate_token():
    user_id = session.get("user_id", "")

    # create serializer with your secret key
    serializer = get_serializer()

    # embed user_id (you can embed more data like email, role, etc.)
    token = serializer.dumps({"user_id": user_id})
    execute(
        sql='UPDATE user SET token = ? WHERE id = ?',
        params=(token, user_id),
        commit=True
    )

    return redirect(url_for('setting'))


def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def verify_token(token: str):
    serializer = get_serializer()
    if not token:
        return "no token found"
    try:
        # max_age = 90 days
        data = serializer.loads(token, max_age=60 * 60 * 24 * 90)
        # return data  # returns the embedded dict, e.g. {"user_id": 1}
        return "valid"
    except SignatureExpired:
        return "token was expired"
    except BadSignature:
        return "token was tampered or invalid"

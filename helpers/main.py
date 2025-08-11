from functools import wraps

from flask import session, flash, url_for, redirect, request


def generate_verification_code():
    import random
    import string
    # Generate a random 6-digit verification code
    return ''.join(random.choices(string.digits, k=6))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.")
            return redirect(url_for("login"))

        # Check if IP matches the one stored during login
        if session.get("ip") != request.remote_addr:
            session.clear()
            flash("Session invalidated due to IP mismatch.")
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function

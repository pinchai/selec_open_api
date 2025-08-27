from functools import wraps

from flask import session, flash, url_for, redirect, request


def generate_verification_code():
    import random
    import string
    # Generate a random 6-digit verification code
    return ''.join(random.choices(string.digits, k=6))


def _client_ip():
    # Respect proxies/load balancers
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr or ""


def _client_browser():
    return f"{request.user_agent}".strip()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(request.user_agent.browser)
        # Not logged in
        if "user_id" not in session:
            flash("Please log in to access this page.")
            return redirect(url_for("login"))

        # IP check (only if we stored it at login)
        sess_ip = session.get("ip")
        if sess_ip is not None and sess_ip != _client_ip():
            session.clear()
            flash("Session invalidated due to IP mismatch.")
            return redirect(url_for("login"))

        # Browser check (only if we stored it at login)
        sess_browser = session.get("browser")
        if sess_browser is not None and sess_browser != _client_browser():
            session.clear()
            flash("Session invalidated due to browser change.")
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function

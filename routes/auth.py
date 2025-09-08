from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from helpers.main import generate_verification_code
from app import app, mail
import sqlite3
from config import *
from flask_mail import Mail, Message


@app.get("/register")
def register():
    return render_template("auth/register.html")


@app.post("/do-register")
def do_register():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    password = generate_password_hash(password)
    gen_code = generate_verification_code()

    if not email or not password:
        flash("Name and Password are required.")
        return redirect(url_for("register"))

    try:
        uid = execute(
            "INSERT INTO user (email, password, verify, verify_code) VALUES (?, ?, ?, ?)",
            (email, password, 0, gen_code)
        )
        msg = Message('FlaskOpenAPI', recipients=[email])
        msg.body = 'Confirm Code.'
        message = render_template('mail/confirm_code.html', code=gen_code)
        msg.html = message
        mail.send(msg)

        resp = redirect(url_for("verify_email"))
        resp.set_cookie("email", f"{email}", max_age=60 * 60 * 24)  # expires in 1 day
        return resp
    except sqlite3.IntegrityError:
        flash("Email already exists.")
        return redirect(url_for("register"))


@app.get("/verify-email")
def verify_email():
    return render_template('auth/verify.html')


@app.get("/login")
def login():
    return render_template("auth/login.html")


@app.post("/do-verify-email")
def do_verify_email():
    email = request.cookies.get("email", "")
    d1 = request.form.get("d1", "").strip()
    d2 = request.form.get("d2", "").strip()
    d3 = request.form.get("d3", "").strip()
    d4 = request.form.get("d4", "").strip()
    d5 = request.form.get("d5", "").strip()
    d6 = request.form.get("d6", "").strip()
    code = f"{d1}{d2}{d3}{d4}{d5}{d6}".strip()

    if not email or not code:
        return f"Email and Code are required."

    user = query("SELECT * FROM user WHERE email = ?", (email,), one=True)
    print(user)
    if not user:
        return "User not found."

    if user["verify"] == 1:
        return redirect(url_for("login"))

    if int(user["verify_code"]) != int(code):
        return 'Invalid verification code.'

    execute("UPDATE user SET verify = 1 WHERE id = ?", (user["id"],))
    return "Email verified successfully!"


@app.post("/do-login")
def do_login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()
    remember = request.form.get("remember") == "on"  # optional checkbox

    if not email or not password:
        flash("Email and Password are required.")
        return redirect(url_for("login"))

    user = query("SELECT * FROM user WHERE email = ?", (email,), one=True)


    if not user:
        flash("User not found.")
        return redirect(url_for("login"))

    if not check_password_hash(user["password"], password):
        flash("Invalid password.")
        return redirect(url_for("login"))

    if user["verify"] == 0:
        flash("Please verify your email first.")
        return redirect(url_for("verify_email"))

    # Clear old session data
    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = 'sample_user'
    session["user_email"] = user["email"]
    session["ip"] = request.remote_addr  # Store login IP
    session["browser"] = f"{request.user_agent}".strip()
    session.permanent = bool(remember)

    flash("Welcome back!")
    return redirect(url_for("admin"))


@app.get("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))

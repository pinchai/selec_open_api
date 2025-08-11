from flask import Flask, render_template
from helpers.main import *
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    SECRET_KEY="dev-secret",
    DATABASE=os.path.join(app.root_path, "flask_open_api.db")
)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'limsopheak703@gmail.com'
app.config['MAIL_PASSWORD'] = 'icpd sqoq reuz npjs'
app.config['MAIL_DEFAULT_SENDER'] = 'limsopheak703@gmail.com'
mail = Mail(app)


@app.get('/sendMail')
def send_mail():
    msg = Message('Hello My Love', recipients=['pinchai.pc@gmail.com'])
    msg.body = 'This is a plain text email sent from Flask.'
    message = render_template('mail/confirm_code.html', code=123456)
    msg.html = message
    try:
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return f'An error occurred: {str(e)}'


# ---------- CLI ----------
import cli.cli
# ---------- Route ----------
import routes


@app.get("/admin")
@login_required
def admin():
    return render_template("admin/dashbord.html")


if __name__ == '__main__':
    app.run()

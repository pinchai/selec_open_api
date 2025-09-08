from datetime import datetime

from flask import Flask, render_template, make_response, jsonify
import pdfkit

from helpers.main import *
import os
from flask_mail import Mail, Message
from flasgger import Swagger
import json
app = Flask(__name__)


# config swagger header
with open("swagger_config.json", "r") as f:
    swagger_template = json.load(f)
swagger = Swagger(app, template=swagger_template)
app.config.update(
    SECRET_KEY="a7bae17a59474ba8cb365edb9feb62b12e4034da0d2529ea3c8b48014a761303",
    # SECRET_KEY=os.urandom(32).hex(),
    DATABASE=os.path.join(app.root_path, "flask_open_api.db")
)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'limsopheak703@gmail.com'
app.config['MAIL_PASSWORD'] = 'icpd sqoq reuz npjs'
app.config['MAIL_DEFAULT_SENDER'] = 'limsopheak703@gmail.com'
mail = Mail(app)


@app.context_processor
def inject_base_url():
    return {
        "base_url": request.url_root.rstrip("/"),
        "get_date_now": datetime.now().strftime("%Y-%m-%d"),
        "get_time_now": datetime.now().strftime("%H:%M:%S"),
    }


@app.errorhandler(Exception)
def error_handler(e):
    return make_response(
        jsonify({"status": "error", "message": str(e)}),
        500
    )


@app.errorhandler(404)
def error_handler(e):
    return make_response(
        jsonify({"status": "page not 404", "message": str(e)}),
        404
    )


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




import cli.cli
import routes

if __name__ == '__main__':
    app.run()

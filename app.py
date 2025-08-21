from datetime import datetime

from flask import Flask, render_template, make_response
import pdfkit

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


@app.context_processor
def inject_base_url():
    return {
        "base_url": request.url_root.rstrip("/"),
        "get_date_now": datetime.now().strftime("%Y-%m-%d"),
        "get_time_now": datetime.now().strftime("%H:%M:%S"),
    }


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


@app.route("/pdf")
def download_pdf_wk():
    html = render_template("POS/invoice.html", title="My Report", rows=[])
    # Point to the wkhtmltopdf binary if not on PATH:
    # config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    options = {
        "page-width": "80mm",
        "page-height": "150mm",
        "encoding": "UTF-8",
        "margin-top": "1mm",
        "margin-right": "1mm",
        "margin-left": "1mm",
        "margin-bottom": "1mm",

        "enable-local-file-access": None,
    }
    pdf_bytes = pdfkit.from_string(html, False, options=options)  # , configuration=config)

    resp = make_response(pdf_bytes)
    resp.headers["Content-Type"] = "application/pdf"
    # Set the Content-Disposition header to prompt download
    # resp.headers["Content-Disposition"] = 'attachment; filename="report.pdf"'

    # Set the Content-Disposition header to display inline
    resp.headers["Content-Disposition"] = 'inline; filename="report.pdf"'
    return resp


# ---------- CLI ----------
import cli.cli
# ---------- Route ----------
import routes

if __name__ == '__main__':
    app.run()

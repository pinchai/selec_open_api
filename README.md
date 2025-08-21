```
flask --app app.py init-db

flask --app app.py truncate-db

flask --app app.py run

```
# selec_open_api


### PDF Generation Doc
```
# OS package needed:
# macOS: brew install wkhtmltopdf
# Ubuntu: sudo apt-get install -y wkhtmltopdf
pip install pdfkit
--------------------
import pdfkit
from flask import Flask, render_template, make_response, request
app = Flask(__name__)
@app.route("/download-pdf-wk")
def download_pdf_wk():
    html = render_template("report.html", title="My Report", rows=[...])
    # Point to the wkhtmltopdf binary if not on PATH:
    # config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    options = {
        "page-size": "A4",
        "margin-top": "16mm",
        "margin-right": "12mm",
        "margin-bottom": "16mm",
        "margin-left": "12mm",
        "encoding": "UTF-8",
        "enable-local-file-access": None,  # allow reading local assets
    }
    pdf_bytes = pdfkit.from_string(html, False, options=options)  # , configuration=config)

    resp = make_response(pdf_bytes)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = 'attachment; filename="report.pdf"'
    return resp
```

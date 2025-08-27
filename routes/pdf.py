import pdfkit
from app import app
from flask import render_template, make_response, request
from config import query, execute


@app.route("/pdf")
def download_pdf_wk():
    sale_id = request.args.get('sale_id', '')
    invoice_type = request.args.get('type', 'inline')

    sale = query('SELECT * FROM sale_order WHERE id = ?', (sale_id,), one=True)
    sale_item = query('SELECT soi.*, p.name FROM sale_order_item soi JOIN product p ON soi.product_id = p.id WHERE soi.order_id = ?', (sale_id,), one=False)
    html = render_template("POS/invoice.html", title="My Report", rows=sale_item, sale=sale)
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
    if invoice_type == 'attachment':
        resp.headers["Content-Disposition"] = f'attachment; filename="invoice_{sale_id}.pdf"'
    elif invoice_type == 'inline':
        resp.headers["Content-Disposition"] = f'inline; filename="invoice_{sale_id}.pdf"'

    return resp

import sqlite3

from flask import Flask, request, jsonify
import json

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('invoices.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn, conn.cursor()


@app.route("/invoices", methods=["GET", "POST"])
def invoices():
    conn, cursor = db_connection()

    if request.method == "GET":
        return invoices_get_all(conn)

    if request.method == "POST":
        new_invoice_num = request.form["invoice_num"]
        new_invoice_series = request.form["invoice_series"]
        new_invoice_type = request.form["invoice_type"]
        new_invoice_client_id = request.form["invoice_client_id"]
        sql = """INSERT INTO invoice
                (invoice_num, invoice_series, invoice_type, client_id)
                VALUES( ?, ?, ?, ?);"""
        cursor = conn.execute(sql, (new_invoice_num, new_invoice_series, new_invoice_type, new_invoice_client_id))
        conn.commit()
        return f"Invoice created succesfully (invoiceid: {cursor.lastrowid})."


@app.route("/invoices/<int:id>", methods=["GET", "DELETE"])
def single_invoice_rd_operations():
    conn, cursor = db_connection()
    invoice = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM invoice WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            invoice = r
        if invoice is None:
            return jsonify({'error': 'Resource not found'}), 404
        return invoice

    if request.method == "DELETE":
        cursor.execute("DELETE FROM invoice WHERE id=?", (id,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({'message': 'Operation was successful'}), 200
        else:
            return jsonify({'message': 'Operation was successful but no invoice to be deleted was found'}), 200


def invoices_get_all(conn):
    cursor = conn.execute("SELECT * FROM invoice")
    return jsonify(cursor.fetchall())


if __name__ == '__main__':
    app.run(debug=True)

'''
@app.route('/')
def index():
    return 'Hello'
'''

'''
@app.route('/<value>')
def print_value(value):
    return 'Routed value: {}'.format(value)
'''

import sqlite3

conn = sqlite3.connect("invoices.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE invoice (
    id integer PRIMARY KEY,
    invoice_num integer NOT NULL,
    invoice_series text NOT NULL,
    invoice_type TEXT CHECK (invoice_type IN ('O', 'C')) NOT NULL,
    invoice_client_id integer NOT NULL
)"""
cursor.execute(sql_query)

# test/sql_injection_psycopg2.py
import os
import psycopg2
from flask import Flask, request

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host="localhost", user="user", password="pass", dbname="appdb"
    )

@app.route("/orders")
def orders():
    user = request.args.get("user", "")
    # Vulnerable: f-string used to construct SQL
    q = f"SELECT id, total FROM orders WHERE user_id = '{user}'"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(q)
    res = cur.fetchall()
    conn.close()
    return {"orders": res}

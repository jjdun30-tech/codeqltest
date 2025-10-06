# test/sql_injection_sqlite.py
import sqlite3
from flask import Flask, request

app = Flask(__name__)
DB = "test.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT);")
    conn.commit()
    conn.close()

@app.route("/item")
def get_item():
    # Vulnerable: unsafely interpolate parameter into SQL
    item_id = request.args.get("id", "1")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    query = f"SELECT name FROM items WHERE id = {item_id};"
    cur.execute(query)  # unsafe when item_id is untrusted
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "not found"

if __name__ == "__main__":
    init_db()
    app.run(port=8083)

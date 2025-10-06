import sqlite3

def get_password(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # Vulnerable: f-string interpolation
    cur.execute(f"SELECT password FROM users WHERE id = {user_id}")
    return cur.fetchone()

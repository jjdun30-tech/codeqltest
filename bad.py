# intentionally-vulnerable.py
# WARNING: This file is intentionally vulnerable. Use only in isolated test environments.

import sqlite3
import os
import shlex

DB = "test.db"

def sqli_v1(username):
    """SQLi #1: naive string concatenation"""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "';"   # <-- SQLi #1
    cur.execute(query)
    return cur.fetchall()

def sqli_v2(user_id):
    """SQLi #2: f-string interpolation"""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"SELECT email FROM users WHERE id = {user_id}")        # <-- SQLi #2
    return cur.fetchone()

def sqli_v3(table, column, value):
    """SQLi #3: format-based construction of a query (also demonstrates unsafe identifier use)"""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    sql = "SELECT {col} FROM {tbl} WHERE name = '{val}'".format(       # <-- SQLi #3 (value) and unsafe identifiers
        col=column, tbl=table, val=value
    )
    cur.execute(sql)
    return cur.fetchall()

def cmd_injection(user_input):
    """CMDi: unsafely building a shell command from user input"""
    # WARNING: using shell=True / os.system with unsanitized input is dangerous
    cmd = "tar -czf /tmp/backup.tar.gz " + user_input   # <-- CMDi: user_input injected into shell command
    # using os.system here to emphasize classic command-injection pattern
    os.system(cmd)
    return True

if __name__ == "__main__":
    # Example (for static analysis only; do not execute with untrusted inputs)
    print("sqli_v1 example:", sqli_v1("alice"))
    print("sqli_v2 example:", sqli_v2("1"))
    print("sqli_v3 example:", sqli_v3("products", "price", "gadget"))
    # cmd_injection(" /var/data ")  # <-- do not run with untrusted input

# codeql-target.py
# Intentionally vulnerable test cases for CodeQL detection — DO NOT RUN IN PRODUCTION.

import sqlite3
import os
import subprocess

DB = "test.db"

def sqli_one():
    # SQLi #1: direct concatenation of tainted input
    name = input("username> ")                      # taint source
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    q = "SELECT * FROM users WHERE username = '" + name + "';"   # vulnerable
    cur.execute(q)
    return cur.fetchall()

def sqli_two():
    # SQLi #2: f-string using tainted input
    uid = input("user id> ")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"SELECT email FROM users WHERE id = {uid}")     # vulnerable
    return cur.fetchone()

def sqli_three(table):
    # SQLi #3: format() with tainted value passed in
    # table name here is **controlled by caller**; caller below uses env var
    col = "description"
    val = os.environ.get("PROD_ITEM", "default")   # taint source from env
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    sql = "SELECT {col} FROM {tbl} WHERE name = '{val}'".format(col=col, tbl=table, val=val)
    cur.execute(sql)   # vulnerable if table or val are attacker-controlled
    return cur.fetchall()

def cmd_inject():
    # CMDi: tainted input appended directly to shell command and executed
    path = input("path> ")                         # taint source
    cmd = "tar -czf /tmp/backup.tar.gz " + path   # vulnerable: shell injection
    # Also demonstrate subprocess.run with shell=True
    subprocess.run(cmd, shell=True)               # sink: shell=True run

if __name__ == "__main__":
    # Caller that wires in the taint for sqli_three using an env var
    # (simulates external, attacker-controlled input)
    os.environ["PROD_ITEM"] = "gadget'; DROP TABLE products; --"
    print("Running sqli_one (static analysis only):", sqli_one())     # static-only: don't give input at runtime
    print("Running sqli_two (static analysis only):", sqli_two())
    print("Running sqli_three (static analysis only):", sqli_three("products"))
    # cmd_inject()  # don't run with untrusted input

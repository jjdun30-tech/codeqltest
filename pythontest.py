# psycopg2_vulns.py
# Intentionally vulnerable — do not run in production.

import os
import psycopg2

DSN = "dbname=test user=test password=test host=localhost"

def sqli_psycopg2_basic():
    # Source: input() -> Sink: cursor.execute with concatenation
    user = input("username> ")                                   # taint source
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    q = "SELECT * FROM users WHERE username = '%s';" % user      # <-- SQLi #1
    cur.execute(q)
    return cur.fetchall()

def sqli_psycopg2_many(records):
    # records is a list of tuples provided by caller (simulating untrusted CSV parsing)
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    # BAD: building multi-row insert by joining strings (instead of parameterized executemany)
    values = ",".join(["('%s','%s')" % (r[0], r[1]) for r in records])  # <-- SQLi #2 if records attacker-controlled
    stmt = "INSERT INTO logins(user, passwd) VALUES " + values + ";"
    cur.execute(stmt)
    conn.commit()

def sqli_psycopg2_identifier(table_name, column, value):
    # Unsafe identifiers + value concatenation
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    # table_name comes from env var to simulate attacker control
    tbl = os.environ.get("TARGET_TABLE", "users")                     # taint source
    sql = f"SELECT {column} FROM {tbl} WHERE note = '{value}'"       # <-- SQLi #3 (identifier + value)
    cur.execute(sql)
    return cur.fetchall()

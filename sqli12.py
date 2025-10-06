import sqlite3

def get_orders(user):
    con = sqlite3.connect("shop.db")
    cur = con.cursor()
    # Vulnerable: chained concatenations
    sql = "SELECT * FROM orders WHERE user = '" + user + "' AND status='active'"
    cur.execute(sql)
    return cur.fetchall()

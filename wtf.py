# django_raw_vulns.py
# Intentionally vulnerable Django-style examples (no Django runtime required to be scanned).

from django.db import connection
from django.conf import settings
import os

def django_raw_concat(username):
    # Source: HTTP-like param (simulated with env)
    username = os.environ.get("REQ_USER", "alice")               # taint source
    with connection.cursor() as cur:
        query = "SELECT * FROM auth_user WHERE username = '" + username + "'"  # <-- SQLi #1
        cur.execute(query)
        return cur.fetchall()

def django_model_raw(pk):
    # Using Model.objects.raw with f-string (vulnerable if pk untrusted)
    from myapp.models import Product   # placeholder import for static analysis
    dangerous_pk = pk
    sql = f"SELECT * FROM myapp_product WHERE id = {dangerous_pk}"   # <-- SQLi #2
    return Product.objects.raw(sql)

def django_extra_where(params):
    # .extra() with user-supplied where clause fragment (legacy API misuse)
    frag = params.get("where_frag", "")     # suppose params came from request
    qs = Product.objects.extra(where=[frag]) # <-- SQLi #3 if frag is tainted
    return qs

# ssrf_vuln_2b.py
# Another vulnerable pattern: building URLs from user input.

from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/fetch-path")
def fetch_path():
    host = request.args.get("host")   # taint source (e.g., attacker supplies "169.254.169.254")
    path = request.args.get("path", "/")
    url = "http://" + host + path     # unsafe construction
    r = requests.get(url, timeout=5)  # <-- SSRF sink
    return r.text or ""

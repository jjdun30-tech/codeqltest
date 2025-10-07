# ssrf_vuln.py
# Purpose: Trigger SSRF / unsafe request construction findings.

import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/fetch")
def fetch_remote():
    # User provides a URL query param: /fetch?url=http://evil.com
    target = request.args.get("url")        # taint source
    # BAD: unvalidated, directly fetched by server
    r = requests.get(target)                # <-- SSRF
    return r.text

if __name__ == "__main__":
    app.run(debug=True)

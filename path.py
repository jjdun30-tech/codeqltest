# archive_extract_vuln.py
# Purpose: Trigger CodeQL's "archive extraction path traversal" (Zip-Slip) rule.

import os
import tarfile
from flask import Flask, request

app = Flask(__name__)
BASE_DIR = "/tmp/uploads"  # pretend deploy dir

@app.route("/upload-tar", methods=["POST"])
def upload_tar():
    # Attacker uploads a .tar with entries like: ../../etc/passwd
    f = request.files["file"]            # taint source (untrusted archive)
    target = os.path.join(BASE_DIR, "extracted")
    os.makedirs(target, exist_ok=True)

    # VULNERABLE: extractall() without validating member names
    with tarfile.open(fileobj=f.stream, mode="r:*") as tf:
        tf.extractall(path=target)       # <-- Zip-Slip / path traversal vuln

    return "ok"

# test/unsafe_yaml_load.py
# Vulnerable: yaml.load on untrusted input can execute arbitrary code via YAML tags
import yaml
from flask import Flask, request

app = Flask(__name__)

@app.route("/import", methods=["POST"])
def import_yaml():
    body = request.get_data(as_text=True) or ""
    data = yaml.load(body, Loader=yaml.Loader)  # ❌ VULNERABLE: unsafe loader
    # Pretend we use the data
    return {"keys": list(data.keys()) if isinstance(data, dict) else []}

if __name__ == "__main__":
    app.run(port=8085)

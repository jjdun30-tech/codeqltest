# test/command_injection_os.py
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        target = q.get("host", ["127.0.0.1"])[0]
        # Vulnerable: user-controlled input interpolated into shell command
        cmd = f"ping -c 1 {target}"
        status = os.system(cmd)  # unsafe when target is untrusted
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Ran: {cmd}\nStatus: {status}".encode())

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8081), Handler).serve_forever()

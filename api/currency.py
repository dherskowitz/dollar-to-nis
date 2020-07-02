import json
import urllib.request
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        base_url = "https://4157pvmbce.execute-api.us-east-1.amazonaws.com"
        path = "/default/dollar-to-nis-prod-getRates"
        data = urllib.request.urlopen(f"{base_url}/{path}").read()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(json.loads(data)).encode())
        return

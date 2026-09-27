import http.server, json, sys
n = int(sys.argv[2])
BODY = json.dumps({"data":[{"id":"ord_%d" % i} for i in range(n)],"meta":{"total":47,"nextCursor":None}}).encode()
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(BODY))); self.end_headers(); self.wfile.write(BODY)
    def log_message(self,*a): pass
http.server.HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()

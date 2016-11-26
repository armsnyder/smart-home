import BaseHTTPServer
import urlparse
import fireplace


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("ok")

    def do_POST(self):
        my_path = urlparse.urlparse(self.path)
        if my_path.path == '/smarthome/fireplace/start':
            fireplace.start()
            self.send_response(200)
            self.end_headers()
            return
        elif my_path.path == '/smarthome/fireplace/stop':
            fireplace.stop()
            self.send_response(200)
            self.end_headers()
            return
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        """merge request body with fireplace state probably via fxn in fireplace.py"""
        self.send_response(200)
        return

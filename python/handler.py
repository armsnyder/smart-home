import BaseHTTPServer
import urlparse

import fireplace


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_PUT(self):
        my_path = urlparse.urlparse(self.path)
        if my_path.path == '/smarthome/fireplace/start':
            self.send_response(fireplace.start())
            self.end_headers()
            return
        elif my_path.path == '/smarthome/fireplace/stop':
            self.send_response(fireplace.stop())
            self.end_headers()
            return
        else:
            self.send_response(404)
            self.end_headers()

import BaseHTTPServer
import json
import re
import socket

import backend.fireplace
import backend.agent_tony

# Response code constants
OK = 200
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
URI_TOO_LONG = 414


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    # noinspection PyAttributeOutsideInit
    def handle_one_request(self):
        """Override implementation from BaseHTTPRequestHandler to call handler methods based on the first part of the
        request path, rather than calling different handler methods based on the request method type"""
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            # handle the request with a different method depending on the first part of the request path
            path_segments = self.path.split('/')
            if len(path_segments) < 3 or path_segments[1] != 'smarthome':
                self.send_response(NOT_FOUND)
            else:
                handler_method_name = 'handle_' + self.path.split('/')[2].lower()
                try:
                    getattr(self, handler_method_name)()
                except AttributeError:
                    self.send_response(NOT_FOUND)
            self.wfile.flush()  # actually send the response if not already done.
        except socket.timeout, e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1

    def handle_google(self):
        match = re.search(r'agents/(\w+)', self.path)
        if not match:
            self.send_response(NOT_FOUND)
            return
        try:
            agent_method = getattr(backend.google_agents, match.group(1))
        except AttributeError:
            self.send_response(NOT_FOUND)
            return
        self.send_header('Google-Assistant-API-Version', 'v1')
        self.send_header('content-type', 'application/json')
        self.send_response(OK)
        self.end_headers()
        request_body = self.rfile.read(int(self.headers.getheader('content-length', 0)))
        response_body = agent_method(json.loads(request_body))
        self.wfile.write(json.dumps(response_body))

    def handle_ifttt(self):
        if self.command == 'HEAD':
            self.send_response(OK)
        elif self.command == 'PUT':
            if 'fireplace/start' in self.path:
                self.send_response(backend.fireplace.start())
            elif 'fireplace/stop' in self.path:
                self.send_response(backend.fireplace.stop())
            elif 'fireplace/feed' in self.path:
                self.send_response(backend.fireplace.feed())
            else:
                self.send_response(NOT_FOUND)
        else:
            self.send_response(METHOD_NOT_ALLOWED)

"""
Routes incoming server HTTP requests into the backend code. This script is tightly coupled with the server.py script.
"""

import BaseHTTPServer
import json
import socket
import os
import sys
import inspect

# add top-level modules to system path so that they can be referenced
cmd_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())),
                                                           os.path.pardir)))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from backend import fireplace
from backend import action

# HTTP response code constants
OK = 200
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
URI_TOO_LONG = 414

# HTTP method type constants
HEAD = 'HEAD'
GET = 'GET'
POST = 'POST'
PUT = 'PUT'


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
        """
        Handle a request coming from the Google Assistant.
        There isn't any logic in this function. Rather, the function takes care of writing the required HTTP headers and
        lets the action.py module handle all of the logic of forming up a response object.
        """
        if self.command == HEAD:
            # it is common practice to send a simple OK with zero processing if the method type is HEAD
            self.send_response(OK)
        elif self.command == POST:
            # All requests from the Google Assistant will be POST requests
            # Write headers for HTTP response
            self.send_header('Google-Assistant-API-Version', 'v1')
            self.send_header('content-type', 'application/json')
            self.send_response(OK)
            self.end_headers()
            # Read the body of the HTTP request that we must handle into a dictionary
            request_body = self.rfile.read(int(self.headers.getheader('content-length', 0)))
            # Get the response body (a JSON string) from the action.py backend module
            response_body = action.respond_to_request(json.loads(request_body))
            # Write the response body into the response
            self.wfile.write(json.dumps(response_body))
        else:
            # any other HTTP method type is not allowed, so return a method-not-allowed HTTP error code
            self.send_response(METHOD_NOT_ALLOWED)

    def handle_ifttt(self):
        """
        Handle a request coming from the IFTTT Maker channel.
        There is logic in this function to call different backend functions depending on what is specified in the
        request URL.
        """
        if self.command == HEAD:
            # it is common practice to send a simple OK with zero processing if the method type is HEAD
            self.send_response(OK)
        elif self.command == PUT:
            # run a different function depending on what is contained in the request URL
            if 'fireplace/start' in self.path:
                self.send_response(fireplace.start())
            elif 'fireplace/stop' in self.path:
                self.send_response(fireplace.stop())
            elif 'fireplace/feed' in self.path:
                self.send_response(fireplace.feed())
            else:
                # if no route is found, return a 404 not found error
                self.send_response(NOT_FOUND)
        else:
            # any other HTTP method type is not allowed, so return a method-not-allowed HTTP error code
            self.send_response(METHOD_NOT_ALLOWED)

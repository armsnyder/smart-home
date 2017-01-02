"""
Opens a server for HTTP and HTTPS traffic. The HTTP request handling happens in the handler.py module.
"""

import ConfigParser
import SocketServer
import os
import ssl
import threading
import inspect

import handler
from backend.config import config
from backend import log

# the default port differs from the actual port used in production so that the code can be tested
# while the production server continues to run
http_port = 8033
https_port = 4433


def main():
    # read ports from config file, if it exists
    configure_ports()
    # start serving both http and https simultaneously
    http_thread = threading.Thread(target=serve_http)
    https_thread = threading.Thread(target=serve_https)
    http_thread.start()
    https_thread.start()
    # wait until both servers are down before exiting
    http_thread.join()
    https_thread.join()


def configure_ports():
    """
    Configure the HTTP and HTTPS ports if they are defined in a config.ini
    """
    global http_port, https_port
    try:
        # if a config value for server port is found, use it
        http_port = config.getint('server', 'http_port')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        # if no config exists, use the default port
        log.warn('No config found. Using default http port.')
    try:
        # if a config value for server port is found, use it
        https_port = config.getint('server', 'https_port')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        # if no config exists, use the default port
        log.warn('No config found. Using default https port.')


def serve_http():
    """
    Bind our handler to a basic HTTP socket and begin serving traffic to it. This method blocks execution until the
    server is shutdown, so it should be called asynchronously as a new process.
    """
    # define a server that runs our handler
    httpd = SocketServer.TCPServer(("", http_port), handler.Handler)
    # start the server
    log.info("Serving HTTP on port " + str(http_port))
    httpd.serve_forever()


def serve_https():
    """
    Bind our handler to a secure HTTPS socket and begin serving traffic to it. This method blocks execution until the
    server is shutdown, so it should be called asynchronously as a new process.
    """
    # define a server that runs our handler
    httpsd = SocketServer.TCPServer(("", https_port), handler.Handler)
    # wrap https socket in ssl
    try:
        # find the system path of the script
        root_path = os.path.realpath(os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe()))))
        # look for ssl keys in a ssl directory, relative to this script, and use them to secure the socket
        httpsd.socket = ssl.wrap_socket(httpsd.socket, keyfile=os.path.join(root_path, 'ssl', 'key.pem'),
                                        certfile=os.path.join(root_path, 'ssl', 'cert.pem'), server_side=True)
    except IOError:
        log.warn("No certificate found. Cannot serve HTTPS.")
        return
    # start the server
    log.info("Serving HTTPS on port " + str(https_port))
    httpsd.serve_forever()


if __name__ == '__main__':
    main()

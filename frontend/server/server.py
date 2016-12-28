#!/usr/bin/env python

import ConfigParser
import SocketServer
import os
import threading
import ssl

import handler
import infrastructure.log

# the default port differs from the actual port used in production so that the code can be tested
# while the production server continues to run
http_port = 8033
https_port = 4433


def main():
    # read ports from config file, if it exists
    configure_ports()
    # start the servers
    http_thread = threading.Thread(target=serve_http)
    https_thread = threading.Thread(target=serve_https)
    http_thread.start()
    https_thread.start()
    # block until both servers are down
    http_thread.join()
    https_thread.join()


def configure_ports():
    global http_port, https_port
    # check if there is a config file that specifies a port to serve on
    root_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(root_path, 'config.ini')
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    try:
        # if a config value for server port is found, use it
        http_port = config.getint('server', 'http_port')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        # if no config exists, use the default port
        infrastructure.log.warn('No config found. Using default http port.')
    try:
        # if a config value for server port is found, use it
        https_port = config.getint('server', 'https_port')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        # if no config exists, use the default port
        infrastructure.log.warn('No config found. Using default https port.')


def serve_http():
    # define a server that runs our handler
    httpd = SocketServer.TCPServer(("", http_port), handler.Handler)
    # start the server
    infrastructure.log.info("Serving HTTP on port " + str(http_port))
    httpd.serve_forever()


def serve_https():
    # define a server that runs our handler
    httpsd = SocketServer.TCPServer(("", https_port), handler.Handler)
    # wrap https socket in ssl
    try:
        root_path = os.path.dirname(os.path.realpath(__file__))
        httpsd.socket = ssl.wrap_socket(httpsd.socket, keyfile=os.path.join(root_path, 'ssl', 'key.pem'),
                                        certfile=os.path.join(root_path, 'ssl', 'cert.pem'), server_side=True)
    except IOError:
        infrastructure.log.warn("No certificate found. Cannot serve HTTPS.")
        return
    # start the server
    infrastructure.log.info("Serving HTTPS on port " + str(https_port))
    httpsd.serve_forever()


if __name__ == '__main__':
    main()

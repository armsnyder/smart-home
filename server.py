import SocketServer
import atexit
import ConfigParser

import handler
import log

# the default port differs from the actual port used in production so that the code can be tested
# while the production server continues to run
DEFAULT_PORT = 8033


def main():
    # check if there is a config file that specifies a port to serve on
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    try:
        # if a config value for server port is found, use it
        selected_port = config.getint('server', 'port')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        # if no config exists, use the default port
        log.warn('No config found. Using default port.')
        selected_port = DEFAULT_PORT
    # define a server that runs our handler
    httpd = SocketServer.TCPServer(("", selected_port), handler.Handler)
    # register the server shutdown function with atexit so it cleans up when the script is exited
    atexit.register(httpd.shutdown)
    log.info("Serving at port " + str(selected_port))
    # start the server
    httpd.serve_forever()


if __name__ == '__main__':
    main()

import SocketServer
import atexit

import handler
import log

PORT = 8032


def main():
    # define a server that runs our handler
    httpd = SocketServer.TCPServer(("", PORT), handler.Handler)
    # register the server shutdown function with atexit so it cleans up when the script is exited
    atexit.register(httpd.shutdown)
    log.info("serving at port " + str(PORT))
    # start the server
    httpd.serve_forever()


if __name__ == '__main__':
    main()

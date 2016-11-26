import SocketServer

import handler
import log

PORT = 8032
httpd = SocketServer.TCPServer(("", PORT), handler.Handler)


def main():
    log.info("serving at port " + str(PORT))
    httpd.serve_forever()


if __name__ == '__main__':
    main()

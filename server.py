import SocketServer
from handler import Handler

PORT = 8032
httpd = SocketServer.TCPServer(("", PORT), Handler)


def main():
    print("serving at port " + str(PORT))
    httpd.serve_forever()


if __name__ == '__main__':
    main()

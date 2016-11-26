import SimpleHTTPServer
import SocketServer

PORT = 8032

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print("serving at port " + str(PORT))
httpd.serve_forever()

#!/usr/bin/env python3.6
import http.server as http
import serverCode
import logging
import socket, sys
import random

homeFiles = '/Users/Jonathan/Documents/GitHub/2019-Project/code/web'
home = sys.path[0]

pyVersion = '3.6.0' # also works: 3.4.0
version = '1.0.0'

logging.basicConfig(filename=home + '/data/info.log', \
                    filemode='a', format='%(asctime)s %(message)s', \
                    level=logging.DEBUG)   

class handleRequest(http.BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.log = logging
        self.client_address = client_address
        self.log.info(str("New request from " + str(client_address[0])))
        
        self.data = None

        super().__init__(request, client_address, server)

    def prep(func):
        def wrapper(self):
            '''Does basic connection things like check the login cookie
            and add the client_address and requestline to the log
            '''
            
            self.requestHeaders = dict(self.headers.items())

            # loginDetails is like a dict
            # 'username' -> str, username of logged in user
            # 'accountType' -> str, 'admin', 'user', or 'removed'
            # 'loggedIn' -> bool, true if logged in, else false
            # 'authentication' -> str, 'sesscookie' or 'usernameandpassword'
            # 'sessCookie' -> str, randomized cookie for login session purposes

            self.log.debug(self.client_address)
            self.log.debug(self.requestline)
            print(self.client_address) # self explanatory, duh
            print(self.requestline) # first line of the http header

            func(self)

        return wrapper 

    @prep
    def do_HEAD(self):
        code, message, data, type_ = serverCode.fetch(self.path[1:])

        self.send_response(code, message)
        self.send_header('Content-type', type_)
        self.end_headers()
        
        self.log.debug("")

    @prep
    def do_GET(self):
        self.serveWebsite()

    def serveWebsite(self):
        if self.path in ['/']:
            self.path = '/index.html'

        print("Serving: " + self.path)

        code, message, data, type_ = serverCode.fetch(self.path[1:], root=homeFiles)

        if isinstance(data, str):
            data = data.encode()

        self.send_response(code, message)
        self.send_header('Content-type', type_)
        
        self.end_headers()
        self.wfile.write(data)
        
        self.log.debug("")


logging.info("Server starting up\n")
if True: # True if only on the machine, False if on the local network
    ip = 'localhost'
else:
    ip = '192.168.10.104' #'192.168.10.143' # ip of serverpi
port = 5000
print(ip + ":"  + str(port))
logging.info("Server on: " + ip + ":" + str(port))

t = http.HTTPServer((ip,port), handleRequest)

try:
    t.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Server shutting down\n")
    logging.info("Server shutting down\n")
    logging.shutdown()

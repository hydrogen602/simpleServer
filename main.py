#!/usr/bin/env python3.7
from __future__ import annotations
import http.server as http
import logging
import sys
import re
import typing

import simpleServer.serverCode as serverCode

# pyVersion = '3.6.0' # also works: 3.4.0
# version = '1.0.0'

homeFiles = ''

def prep(func: typing.Callable[[handleRequest], None]):
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

        func(self)

    return wrapper


class handleRequest(http.BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.log = logging
        self.client_address = client_address
        self.log.info("New request from " + str(client_address[0]))

        self.data = None

        super().__init__(request, client_address, server)

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
        if self.path.endswith('/'):
            self.path += 'index.html'

        # if self.path.split('/')[-1].find('.') == -1:
        #    self.path = f"{self.path}.html"

        self.log.debug("Serving: " + self.path)

        code, message, data, type_ = serverCode.fetch(self.path[1:],
                                                      root=homeFiles
                                                      )

        if isinstance(data, str):
            data = data.encode()

        self.send_response(code, message)
        self.send_header('Content-type', type_)

        self.end_headers()
        self.wfile.write(data)

        self.log.debug("")


logging.basicConfig(filename='info.log',
                    filemode='a', format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


def start(path: str, ip: str, port: int):
    logging.info("Server starting up\n")

    global homeFiles
    homeFiles = path

    print(ip + ":" + str(port))
    logging.info("Server on: " + ip + ":" + str(port))

    t = http.HTTPServer((ip, port), handleRequest)

    try:
        t.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Server shutting down\n")
        logging.info("Server shutting down\n")
        logging.shutdown()


def printUsage():
    print("main.py folder [ip port]")


if __name__ == '__main__':
    if len(sys.argv) not in [2, 4]:
        printUsage()
        sys.exit(1)

    ip: str = ''
    port: int = 0

    homeFiles = sys.argv[1]

    if len(sys.argv) == 4:
        regex = '^((\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})|localhost)$'
        m = re.match(regex, sys.argv[2])
        if not m:
            print('ip not in correct format')
            printUsage()
            sys.exit(1)

        ip = m.group()

        if sys.argv[3].isnumeric() and int(sys.argv[3]) > 0:
            port = int(sys.argv[3])
        else:
            print('port must be a positive integer')
            printUsage()
            sys.exit(1)
    else:
        ip = 'localhost'
        port = 8080

    start(homeFiles, ip, port)

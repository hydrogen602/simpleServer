#!/usr/bin/env python3.7
'''Main part of simpleServer
Call `start`
or run
    ./main.py folder ip port
in bash'''

from __future__ import annotations
import http.server as http
import logging
from logging.handlers import RotatingFileHandler
import sys
import re
import typing

if __name__ == '__main__':
    from serverCode import fetch
else:
    from .serverCode import fetch

# pyVersion = '3.6.0' # also works: 3.4.0
# version = '1.0.0'

homeFiles = ''
'''The path to the files to be served'''


def prep(func: typing.Callable[[handleRequest], None]):
    '''Only for use with handleRequest.
    Preparse a request response by getting the
    headers and logs the connecting address and request'''

    def wrapper(self):
        '''Does basic connection things like check the login cookie
        and add the client_address and requestline to the log
        '''

        self.requestHeaders = dict(self.headers.items())

        self.log.debug(self.client_address)
        self.log.debug(self.requestline)

        func(self)

    return wrapper


class handleRequest(http.BaseHTTPRequestHandler):
    '''Extends `http.BaseHTTPRequestHandler` and handles incoming requests'''

    def __init__(self, request, client_address, server):
        '''Called by the `http` module and
        shouldn't be called by anything else'''

        self.log = log
        self.client_address = client_address
        self.log.info("New request from " + str(client_address[0]))

        self.data = None

        super().__init__(request, client_address, server)

    @prep
    def do_HEAD(self):
        '''Serves a HEAD request'''

        code, message, data, type_ = fetch(self.path[1:])

        self.send_response(code, message)
        self.send_header('Content-type', type_)
        self.end_headers()

        self.log.debug("")

    @prep
    def do_GET(self):
        '''Serves a GET request'''
        self.serveWebsite()

    def serveWebsite(self):
        '''Fetches the requested file and writes it as
        `http.BaseHTTPRequestHandler` requires.
        This should be the last method called in the
        instances life'''

        if self.path.endswith('/'):
            self.path += 'index.html'

        # if self.path.split('/')[-1].find('.') == -1:
        #    self.path = f"{self.path}.html"

        self.log.debug("Serving: " + self.path)

        code, message, data, type_ = fetch(self.path[1:],
                                           root=homeFiles
                                           )

        if isinstance(data, str):
            data = data.encode()

        self.send_response(code, message)
        self.send_header('Content-type', type_)

        self.end_headers()
        self.wfile.write(data)

        self.log.debug("")


my_handler = RotatingFileHandler('info.log', mode='a', maxBytes=50*1024,  # 50K
                                 backupCount=2, encoding=None, delay=0)

log_formatter = logging.Formatter('%(asctime)s %(message)s')

# logging.basicConfig(filename='info.log',
#                     filemode='a', format='%(asctime)s %(message)s',
#                     level=logging.DEBUG)

my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)

log.addHandler(my_handler)


def start(path: str, ip: str, port: int):
    '''Starts the server
    Args:
        path (str): The path to the files being served
        ip   (str): The ip address or localhost
        port (int): The port number
    '''

    log.info("Server starting up\n")

    global homeFiles
    homeFiles = path

    print(ip + ":" + str(port))
    log.info("Server on: " + ip + ":" + str(port))

    t = http.HTTPServer((ip, port), handleRequest)

    try:
        t.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Server shutting down\n")
        log.info("Server shutting down\n")
        logging.shutdown()


def printUsage():
    '''Prints how to use main.py as a command'''
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

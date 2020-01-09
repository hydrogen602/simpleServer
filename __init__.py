'''Main part of simpleServer
Serves static pages for helping devloping webpages
that can't be loaded in the browser because they use
XMLHttpRequests or something of a similar manner
import simpleServer as a module and then call `start`
or run
    ./main.py folder ip port
in bash'''
from .main import start, handleRequest # NOQA

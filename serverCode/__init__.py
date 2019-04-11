if __name__ == '__main__':
    pass
elif __name__ == '__init__':
    raise ImportError('This module is only for initializing packages')
else:
    from sys import path
    path += __path__

from fileLoader import fetch

import jsonHandler

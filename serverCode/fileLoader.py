
errorMsg = '''<!DOCTYPE html>
<html>
    <head>
        <title>Error</title>
    </head>
    <body>
        <h1>Server Error!</h1>
        <p>We apologize for the inconvenience</p>
        <p>{0}</p>
    </body>
</html>'''
'''Simple error message as html'''

fileTypes = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "text/javascript",
    ".xml": "text/xml",
    ".txt": "text/txt",
    ".png": "image/png",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".gif": "image/gif",
    ".ico": "image/png"
}
'''MIME for common file extensions'''


def fetch(file, root=None) -> (int, str, str, str):
    '''Fetches a file
    Returns 404 if the file isn't found and DOES NOT throw an exception

    Args:
        file (str): The name of the file to get
        root (str, optional, default=None): The location to look for the file

    Returns:
        (codeMsg, textMsg, file, type): codeMsg is the HTTP status code,
        testMsg is the HTTP status description like OK or Forbidden
        file is the actual contents of the file, in bytes or as a string
        type is the media type (file type)
    '''
    'returns codeMsg, textMsg, file, type'
    if '..' in file:
        return 400, 'Bad Request', errorMsg, 'text/html'

    path = str(file)
    if path[path.rfind('.'):] not in fileTypes:
        type_ = '.html'
    else:
        type_ = path[path.rfind('.'):]
    type_ = fileTypes[type_]

    if root:
        absPath = root + '/' + path
    else:
        absPath = path

    try:
        if type_ == 'image/png':
            f = open(absPath, 'rb')
        else:
            f = open(absPath)
        msg = f.read()
        f.close()
    except FileNotFoundError:
        return 404, 'File not found', errorMsg.format(path), 'text/html'
    except IsADirectoryError:
        return 403, 'Forbidden', errorMsg.format(path), 'text/html'

    return 200, 'OK', msg, type_

import jsonHandler as json

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

fileTypes = json.load('fileTypes')

def fetch(file, root=None) -> (int, str, str, str):
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
        '''
        print('Encountered directory, serving index.html instead')
        if not absPath.endswith('/'):
            absPath += '/'
        absPath += 'index.html'
        
        try:
            f = open(absPath)
            msg = f.read()
            f.close()
        except FileNotFoundError:
            return 404, 'File not found', errorMsg.format(path), 'text/html'
        '''
    return 200, 'OK', msg, type_

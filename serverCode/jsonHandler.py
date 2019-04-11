import json

#path = '../data/'
import sys
path = sys.path[0]
if path.endswith('serverCode'):
    path = path[:-11]

path += '/data/'

# using json

def dump(obj, name):
    'args: iterable, name: string'
    file = path + '{0}.json'.format(name)
    s = json.dumps(obj, indent=4)
    f = open(file, 'w')
    f.write(s)
    f.close()

def load(name):
    file = path + '{0}.json'.format(name)
    f = open(file, 'r')
    s = f.read()
    f.close()
    return json.loads(s)

def listFiles():
    from os import chdir, listdir
    chdir(path)
    ls = []
    for i in listdir():
        if i.endswith('.json'):
            ls.append(i)
    return ls
    

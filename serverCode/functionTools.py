# enforce is a decorator, use @enforce

# updated 2018-05-03, date format: ISO 8601

def enforce(func):
    '''to enforce argument and return types'''
    def wrapper(*args):
        a = func.__annotations__.copy()
        tmp = args
        #print(a)
        #print(args)
        if 'self' in a:
            a.pop('self')
            #args = args[1:]
        
        if 'return' not in a:
            raise TypeError("Return type not specified")
        returnType = a.pop('return')
        
        #if len(a) != len(args):
        #    raise TypeError("Wrong arguments given")
        for i, arg in zip(a, args):
            if a[i] != type(arg):
                raise TypeError("Wrong arguments given, expected {0}, got {1}".format(a[i], type(arg)))
        result = func(*tmp)
        if returnType != type(result):
            raise TypeError("Wrong return type")
        return result
    
    wrapper.__doc__ = doc(func)
    wrapper.__name__ = func.__name__
    return wrapper
            
def doc(func):
    s = ''
    #s = 'Help on function {0} in module {1}:\n\n'.format(func.__name__, func.__module__)
    a = func.__annotations__.copy()
    returns = None
    if 'return' in a:
        returns = a.pop('return')

    ls = []
    for i in a:
        ls.append(i + ': ' + str(a[i]))
    #s += '{0}({1})\n'.format(func.__name__, ', '.join(ls))
    s += 'args: {0}\n'.format(', '.join(ls))
    if bool(returns):
            s += 'returns: ' + str(returns) + '\n'
    if func.__doc__ != None:
        s += func.__doc__ + '\n'
    return s

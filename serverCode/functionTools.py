# enforce is a decorator, use @enforce

# updated 2018-05-03


def enforce(func):
    '''to enforce argument and return types'''
    def wrapper(*args):
        a = func.__annotations__.copy()
        tmp = args

        if 'self' in a:
            a.pop('self')

        if 'return' not in a:
            raise TypeError("Return type not specified")
        returnType = a.pop('return')

        for i, arg in zip(a, args):
            if a[i] != type(arg):
                raise TypeError(f"Wrong type, expected {a[i]}, got {arg}")

        result = func(*tmp)
        if returnType != type(result):
            raise TypeError("Wrong return type")
        return result

    wrapper.__doc__ = doc(func)
    wrapper.__name__ = func.__name__
    return wrapper


def doc(func):
    s = ''
    a = func.__annotations__.copy()
    returns = None
    if 'return' in a:
        returns = a.pop('return')

    ls = []
    for i in a:
        ls.append(i + ': ' + str(a[i]))
    # s += '{0}({1})\n'.format(func.__name__, ', '.join(ls))
    s += 'args: {0}\n'.format(', '.join(ls))
    if bool(returns):
        s += 'returns: ' + str(returns) + '\n'
    if func.__doc__ is not None:
        s += func.__doc__ + '\n'
    return s

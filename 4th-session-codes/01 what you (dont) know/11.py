
################# Easy #####################
def function_wrapper(fun):
    return fun


def function():
    pass


function = function_wrapper(function)


################# Suger #####################


def function_wrapper(fun):
    return fun


@function_wrapper
def function():
    pass


################# Classy #####################


class FunctionWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


@FunctionWrapper
def function():
    pass



################# Onion #####################


def function_wrapper(wrapped):
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    _wrapper.__name__ = wrapped.__name__
    _wrapper.__doc__ = wrapped.__doc__
    return _wrapper


@function_wrapper
def function():
    """Hello"""
    pass


################# Salt #####################


import functools


def function_wrapper(wrapped):
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    return _wrapper


@function_wrapper
def function():
    pass


################# Pepper #####################


import functools


class function_wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        functools.update_wrapper(self, wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


@function_wrapper
def function():
    pass

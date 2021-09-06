# We have:
# Preservation of function __name__ and __doc__ and ...
# Preservation of function argument specification.
# Preservation of ability to get function source code.
# Ability to apply decorators on top of other decorators that are implemented as descriptors.


class object_proxy:

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__name__ = wrapped.__name__
        except AttributeError:
            pass

    @property
    def __class__(self):
        return self.wrapped.__class__

    def __getattr__(self, name):
        return getattr(self.wrapped, name)



class bound_function_wrapper(object_proxy):

    def __init__(self, wrapped):
        super(bound_function_wrapper, self).__init__(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


class function_wrapper(object_proxy):

    def __init__(self, wrapped):
       super(function_wrapper, self).__init__(wrapped)

    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__(instance, owner)
        return bound_function_wrapper(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


# Nice to have:
# @decorator
# def my_function_wrapper(wrapped, args, kwargs):
#     return wrapped(*args, **kwargs)
#
# @my_function_wrapper
# def function():
#     pass


import functools


def decorator(wrapper):
    @functools.wraps(wrapper)
    def _decorator(wrapped):
        return function_wrapper(wrapped, wrapper)
    return _decorator


class bound_function_wrapper(object_proxy):

    def __init__(self, wrapped, wrapper):
        super(bound_function_wrapper, self).__init__(wrapped)
        self.wrapper = wrapper

    def __call__(self, *args, **kwargs):
        return self.wrapper(self.wrapped, args, kwargs)


class function_wrapper(object_proxy):

    def __init__(self, wrapped, wrapper):
        super(function_wrapper, self).__init__(wrapped)
        self.wrapper = wrapper

    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__(instance, owner)
        return bound_function_wrapper(wrapped, self.wrapper)

    def __call__(self, *args, **kwargs):
        return self.wrapper(self.wrapped, args, kwargs)





# @my_function_wrapper
# def function(a, b):
#     pass
#
#
# function(1, 2)



@decorator
def my_function_wrapper(wrapped, args, kwargs):
    print('ARGS', args)
    return wrapped(*args, **kwargs)

class Class(object):
    @my_function_wrapper
    def function_im(self, a, b):
        pass


c = Class()
c.function_im(1, 3)

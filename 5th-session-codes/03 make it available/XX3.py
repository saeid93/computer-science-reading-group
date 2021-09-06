import functools
import inspect


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

    def __init__(self, wrapped, instance, wrapper):
        super(bound_function_wrapper, self).__init__(wrapped)
        self.instance = instance
        self.wrapper = wrapper

    def __call__(self, *args, **kwargs):
        return self.wrapper(self.wrapped, self.instance, args, kwargs)


class function_wrapper(object_proxy):

    def __init__(self, wrapped, wrapper):
        super(function_wrapper, self).__init__(wrapped)
        self.wrapper = wrapper

    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__(instance, owner)
        return bound_function_wrapper(wrapped, instance, self.wrapper)

    def __call__(self, *args, **kwargs):
        return self.wrapper(self.wrapped, None, args, kwargs)


def decorator(wrapper):
    @functools.wraps(wrapper)
    def _decorator(wrapped):
        return function_wrapper(wrapped, wrapper)
    return _decorator


@decorator
def my_function_wrapper(wrapped, instance, args, kwargs):
    print('INSTANCE', instance)
    print('ARGS', args)
    return wrapped(*args, **kwargs)


@my_function_wrapper
def function(a, b):
    pass


# function(1, 2)


class Class(object):
    @my_function_wrapper
    def function_im(self, a, b):
        pass


# c = Class()
# c.function_im(1, 2)
# Class.function_im(c, 1, 2)


@decorator
def universal(wrapped, instance, args, kwargs):
    if instance is None:
        if inspect.isclass(wrapped):
            ...  # class.
        else:
            ...  # function or staticmethod.
    else:
        if inspect.isclass(instance):
            ...  # classmethod.
        else:
            ...  # instancemethod.


class Class:

    @my_function_wrapper
    @classmethod
    def function_cm(self, a, b):
        pass

    @my_function_wrapper
    @staticmethod
    def function_sm(a, b):
        pass

Class.function_cm(1, 2)
Class.function_sm(1, 2)

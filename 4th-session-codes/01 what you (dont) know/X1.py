import functools


class function_wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        functools.update_wrapper(self, wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)





# class Class(object):
#
#     @function_wrapper
#     def method(self):
#         pass
#
#     @classmethod
#     def cmethod(cls):
#         pass
#
#     @staticmethod
#     def smethod():
#         pass
#
#
# c = Class()          # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# c.method()


def function_wrapper(wrapped):
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        nonlocal wrapped
        if isinstance(wrapped, classmethod):
            wrapped = wrapped.__func__
        return wrapped(object(), *args, **kwargs)
    return _wrapper

class Class(object):
    @function_wrapper
    @classmethod
    def cmethod(cls):
        pass

Class.cmethod()        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#
#
# class Class(object):
#     @function_wrapper
#     @classmethod
#     def cmethod(cls):
#         pass
#
# # Class.cmethod()        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

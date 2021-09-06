import functools
################# What are descriptors? #####################
# Learning about descriptors not only provides access to a larger
# toolset, it creates a deeper understanding of how Python works
# and an appreciation for the elegance of its design.
# --Raymond Hettinger

# >>> def f(inp): pass
#
# >>> hasattr(f, '__get__')
# True
#
# >>> f
# <function f at 0x10e963cf8>
#
# >>> obj = object()
#
# >>> f.__get__(obj, type(obj))
# <bound method object.f of <object object at 0x10e8ac0b0>>

# class A:
#     def f(self):
#         print('hi')
#
# a = A()
# a.f()  # ---> f.__get__(a, A)()

# class Object(object):
#     def f(self): pass
#
#
# obj = Object()
# print(obj.f)


################# Descriptor as decorator #####################


# class bound_function_wrapper:
#
#     def __init__(self, wrapped):
#         self.wrapped = wrapped
#         functools.update_wrapper(self, wrapped)
#
#     def __call__(self, *args, **kwargs):
#         return self.wrapped(*args, **kwargs)
#
#
# class function_wrapper:
#
#     def __init__(self, wrapped):
#         self.wrapped = wrapped
#         functools.update_wrapper(self, wrapped)
#
#     def __get__(self, instance, owner):
#         wrapped = self.wrapped.__get__(instance, owner)
#         return bound_function_wrapper(wrapped)
#
#     def __call__(self, *args, **kwargs):
#         return self.wrapped(*args, **kwargs)
#
#
# class Class(object):
#     @function_wrapper
#     @classmethod
#     def cmethod(cls):
#         pass
#
# Class.cmethod()
# print("wow it works!")


################## A transparent decorator #####################


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

# Class.cmethod # -----> Class.__getattr__('cmethod')

class bound_function_wrapper(object_proxy):

    def __init__(self, wrapped):
        super().__init__(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


class function_wrapper(object_proxy):

    def __init__(self, wrapped):
        super().__init__(wrapped)

    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__(instance, owner)
        return bound_function_wrapper(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


class Class(object):
    @function_wrapper
    @classmethod
    def cmethod(cls):
        pass

Class.cmethod()
print('it works')


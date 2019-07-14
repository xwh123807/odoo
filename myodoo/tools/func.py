from functools import wraps
from inspect import getsourcefile
from json import JSONEncoder


class lazy_property(object):
    def __int__(self, fget):
        pass

    def __get__(self, obj, cls):
        pass

    @property
    def __doc__(self):
        pass

    @staticmethod
    def reset_all(obj):
        pass


class lazy_classproperty(lazy_property):
    def __get__(self, obj, cls):
        pass


def conditional(condition, decorator):
    pass


def sychronized(lock_attr='_lock'):
    pass


def frame_codeinfo(fframe, back=0):
    pass


def compose(a, b):
    pass


class _ClassProperty(property):
    def __get__(self, instance, owner):
        return self.fget.__get__(None, owner)()


def classproperty(func):
    return _ClassProperty(classmethod(func))


class lazy(object):
    def __int__(self):
        pass

    def _value(self):
        pass

    def __getattr__(self, item):
        pass

    def __setattr__(self, key, value):
        pass

    def __delattr__(self, item):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __bytes__(self):
        pass

    def __format__(self, format_spec):
        pass


def default(self, o):
    pass


json_encoder_default = JSONEncoder.default
JSONEncoder.default = default

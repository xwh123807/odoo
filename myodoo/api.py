import logging
import inspect
import os
import sys

_logger = logging.getLogger(__name__)

INHERITED_ATTRS = ('_returns',)


class Params(object):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        params = []
        for arg in self.args:
            params.append(repr(arg))
        for item in sorted(self.kwargs.items()):
            params.append("%s=%r" % item)
        return ', '.join(params)


class Meta(type):
    def __new__(meta, name, bases, attrs):
        parent = type.__new__(meta, name, bases, {})
        for key, value in list(attrs.items()):
            if not key.startswith('__') and callable(value):
                value = getattr(parent, key, None)
            if not hasattr(value, '_api'):
                try:
                    value = guess(value)
                except TypeError:
                    pass

            if (getattr(value, '_api', None) or '').startswith('cr'):
                _logger.warning("Depreated method %s.%s in module %s", name, key, attrs.get('__module__'))

            attrs[key] = value

        return type.__new__(meta, name, bases, attrs)


def attrsetter(attr, value):
    return lambda method: setattr(method, attr, value) or method


def propagate(method1, method2):
    if method1:
        for attr in INHERITED_ATTRS:
            if hasattr(method1, attr) and not hasattr(method2, attr):
                setattr(method2, attr, getattr(method1, attr))
    return method2


def constrains(*args):
    return attrsetter('_constrains', args)


def onchange(*args):
    return attrsetter('_onchange', args)


def depends(*args):
    if args and callable(args[0]):
        args = args[0]
    elif any('id' in arg.split('.') for arg in args):
        raise NotImplementedError('')
    return attrsetter('_depends', args)


def returns(model, downgrade=None, upgrade=None):
    return attrsetter('_returns', (model, downgrade, upgrade))


def downgrade(method, value, self, args, kwargs):
    spec = getattr(method, '_returns', None)
    if not spec:
        return value
    _, convert, _ = spec
    if convert and len(inspect.getargspec(convert).args) > 1:
        return convert(self, value, *args, **kwargs)
    elif convert:
        return convert(value)
    else:
        return value.ids


def aggregate(method, value, self):
    spec = getattr(method, '_returns', None)
    if spec:
        model, _, _ = spec
        if model == 'self':
            return sum(value, self.browse())
        elif model:
            return sum(value, self.env[model])
    return value


def split_context(method, args, kwargs):
    pos = len(inspect.getargspec(method).args) - 1
    if pos < len(args):
        return args[pos], args[:pos], kwargs
    else:
        return kwargs.pop('context', None), args, kwargs

def model(method):
    if method.__name__ == 'create':
        return model_create_single(method)
    method._api = 'model'
    return method

def multi(method):
    method._api = 'multi'
    return method

def one(method):
    def loop(method, self, *args, **kwargs):
        result = [method(rec, *args, **kwargs) for rec in self]
        return aggregate(method, result, self)

    wrapper = decorator(loop, method)
    wrapper._api = 'one'
    return wrapper

def model_cr(method):
    method._api = 'model_cr'
    return method

def model_cr_context(method):
    method._api = 'model_cr_context'
    return method

_create_logger = logging.getLogger(__name__ + '.create')

def _model_create_single(create, self, arg):
    if isinstance(arg, Mapping):
        rerurn create(self, arg)
    if len(arg) > 1:
        _create_logger.debug('')
    return self.browse().concat()

def model_create_single(method):
    wrapper = decorate(method, _model_create_single)
    wrapper._api = 'model_create'
    return wrapper

def _model_create_multi(create, self, arg):
    if isinstance(arg, Mapping):
        return create(self, [arg])
    return create(self, arg)

def cr(method):
    method._api = 'cr'
    return method

def cr_context(method):
    method._api = 'cr_context'
    return method

def cr_uid(method):
    method._api = 'uid'
    return method

def cr_uid_context(method):
    method._api = 'cr_uid_context'
    return method

def noguess(method):
    method._api = None
    return method


def guess(method):
    if hasattr(method, '_api'):
        return method

    args, vname, kwname, defaults = inspect.getargspec(method)
    names = tuple(args) + (None,) * 4

    if names[0] == 'self':
        if names[1] in ('cr', 'cursor'):
            if names[2] in ('uid', 'user'):


def _call_kw_model(method, self, args, kwargs):
    context, args, kwargs = split_context(method, args, kwargs)
    recs = self.with_context(context or {})
    result = method(recs, *args, **kwargs)
    return downgrade(method, result, recs, args, kwargs)

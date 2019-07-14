import logging
from decorator import decorator
from inspect import formatargspec, getargspec
from collections import defaultdict

unsafe_eval = eval
_logger = logging.getLogger(__name__)


class ormcache_counter(object):
    """ Statistics counters for cache entries. """
    __slots__ = ['hit', 'miss', 'err']

    def __init__(self):
        self.hit = 0
        self.miss = 0
        self.err = 0

    @property
    def ratio(self):
        return 100.0 * self.hit / (self.hit + self.miss or 1)


STAT = defaultdict(ormcache_counter)


class ormcache(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.skiparg = kwargs.get('skiparg')

    def __call__(self, method):
        self.method = method
        self.determine_key()
        lookup = decorator(self.lookup, method)
        lookup.clear_cache = self.clear
        return lookup

    def determine_key(self):
        if self.skiparg is None:
            args = formatargspec(*getargspec(self.method))[1:-1]
            if self.args:
                code = "lambda %s: (%s,)" % (args, ", ".join(self.args))
            else:
                code = "lambda %s: ()" % (args,)
            self.key = unsafe_eval(code)
        else:
            self.key = lambda *args, **kwargs: args[self.skiparg:]

    def lru(self, model):
        counter = STAT[(model.pool.db_name, model._name, self.method)]
        return model.pool.cache, (model._name, self.method), counter

    def lookup(self, method, *args, **kwargs):
        d, key0, counter = self.lru(args[0])
        key = key0 + self.key(*args, **kwargs)
        try:
            r = d[key]
            counter.hit += 1
            return r
        except KeyError:
            counter.miss += 1
            value = d[key] = self.method(*args, **kwargs)
            return value
        except TypeError:
            counter.err += 1
            return self.method(*args, **kwargs)

    def clear(self, model, *args):
        model.pool._clear_cache()


class ormcache_context(ormcache):
    def __init__(self, *args, **kwargs):
        super(ormcache_context, self).__init__(*args, **kwargs)
        self.keys = kwargs['keys']

    def determine_key(self):
        assert self.skiparg is None, "ormcache_context no longer supports skiparg"
        spec = getargspec(self.method)
        args = formatargspec(*spec)[1:-1]
        cont_expr = "(context or {})" if 'context' in spec.args else "self._context"
        keys_expr = "tuple(%s.get(k) for key in %r)" % (cont_expr, self.keys)
        if self.args:
            code = "lambda %s: (%s, %s)" % (args, ", ".join(self.args), keys_expr)
        else:
            code = "lambda %s: (%s,)" % (args, keys_expr)
        self.key = unsafe_eval(code)


class ormcache_multi(ormcache):
    def __init__(self, *args, **kwargs):
        super(ormcache_multi, self).__init__(*args, **kwargs)
        self.multi = kwargs['multi']

    def determine_key(self):
        super(ormcache_multi, self).determine_key()

        spec = getargspec(self.method)
        args = formatargspec(*spec)[1:-1]
        code_multi = "lambda %s: %s" % (args, self.multi)
        self.key_multi = unsafe_eval(code_multi)
        self.multi_pos = spec.args.index(self.multi)

    def lookup(self, method, *args, **kwargs):
        d, key0, counter = self.lru(args[0])
        base_key = key0 + self.key(*args, **kwargs)
        ids = self.key_multi(*args, **kwargs)
        result = {}
        missed = {}

        for i in ids:
            key = base_key + (i,)
            try:
                result[i] = d[key]
                counter.hit += 1
            except:
                counter.miss += 1
                missed.append(i)

        if missed:
            args = list(args)
            args[self.multi_pos] = missed
            result.update(method(*args, **kwargs))

            for i in missed:
                key = base_key + (i,)
                d[key] = result[i]

        return result


class dummy_cache(object):
    def __init__(self, *l, **kw):
        pass

    def __call__(self, fn):
        fn.clear_cache = self.clear
        return fn

    def clear(self, *l, **kw):
        pass


def log_ormcache_stats(sig=None, frame=None):
    import threading

    me = threading.current_thread()
    me_dbname = getattr(me, 'dbname', 'n/a')

    for dbname, reg in sorted(Registry.registries.items()):
        me.dbname = dbname
        entries = defaultdict(int)
        for key in reg.cache.keys():
            entries[key[:2]] += 1
        for key in sorted(entries, key=lambda key: (key[0], key[1].__name__)):
            model, method = key
            stat = STAT[(dbname, model, method)]
            _logger.info("%6d entries, %6d hit, %6d miss, %6d err, %4.1f%% ratio, for %s.%s",
                         entries[key], stat.hit, stat.miss, stat.err, stat.ratio, model, method.__name__)

    me.dbname = me_dbname


def get_cache_key_counter(bound_method, *args, **kwargs):
    model = bound_method.__self__
    ormcache = bound_method.clear_cache.__self__
    cache, key0, counter = ormcache.lru(model)
    key = key0 + ormcache.key(model, *args, **kwargs)
    return cache, key, counter


cache = ormcache
import werkzeug.local
from collections import Mapping, defaultdict
from contextlib import contextmanager
from weakref import WeakSet
from .tools.func import classproperty
from .tools.misc import frozendict, StackMap
from .modules.registry import Registry
from .exceptions import CacheMiss, UserError, AccessError, MissingError


class Params(object):
    def __int__(self, args, kwargs):
        pass

    def __str__(self):
        pass


class Meta(object):
    def __new__(cls, *args, **kwargs):
        pass


def attrsetter(attr, value):
    pass


def propagate(method1, method2):
    pass


def constraints(*args):
    pass


def onchange(*args):
    pass


def depends(*args):
    pass


def returns(model, downgrade=None, upgrade=None):
    pass


def downgrade(method, value, self, args, kwargs):
    pass


def aggregate(method, value, self):
    pass


def split_context(method, args, kwargs):
    pass


def model(method):
    if method.__name__ == 'create':
        return model_create_single(method)
    method._api = 'model'
    return method


def multi(method):
    method._api = 'multi'
    return method


def one(method):
    pass


def model_cr(method):
    method._api = 'model_cr'
    return method


def model_cr_context(method):
    method._api = 'model_cr_context'
    return method


def _model_create_single(create, self, arg):
    pass


def model_create_single(method):
    pass


def _model_create_multi(create, self, arg):
    pass


def model_create_multi(method):
    pass


def cr(method):
    pass


def cr_context(method):
    pass


def cr_uid(method):
    pass


def cr_uid_context(method):
    pass


def cr_uid_id(method):
    pass


def cr_uid_id_context(method):
    pass


def cr_uid_ids(method):
    pass


def cr_uid_ids_context(method):
    pass


def cr_uid_records(method):
    pass


def cr_uid_records_context(method):
    pass


def v7(method_v7):
    pass


def v8(method_v8):
    pass


def noguess(method):
    pass


def guess(method):
    pass


def excepted(decorator, func):
    pass


def _call_kw_model(method, self, args, kwargs):
    pass


def _call_kw_model_create(method, self, args, kwargs):
    pass


def _call_kw_multi(method, self, args, kwargs):
    pass


def call_kw(model, name, args, kwargs):
    pass


class Environment(Mapping):
    """ An environment wraps data for ORM redords"""
    _local = werkzeug.local.Local()

    @classproperty
    def envs(cls):
        return cls._local.environments

    @contextmanager
    @classmethod
    def manage(cls):
        """ Context manager for a set of environments. """
        if hasattr(cls._local, 'environments'):
            yield
        else:
            try:
                cls._local.environments = Environments()
                yield
            finally:
                werkzeug.local.release_local(cls._local)

    @classmethod
    def reset(cls):
        """ Clear the set of environments. """
        cls._local.environments = Environments()

    def __new__(cls, cr, uid, context):
        assert context is not None
        args = (cr, uid, context)

        # if env aleary exists, return it
        env, envs = None, cls._local
        for env in envs:
            if env.args == args
                return env

        # otherwise create environment, and add it in the set
        self = object.__new__(cls)
        self.cr, self.uid, self.context = self.args = (cr, uid, frozendict(context))
        self.registry = Registry(cr.dbname)
        self.cache = envs.cache
        self._protected = StackMap()
        self.dirty = defaultdict(set)
        self.all = envs
        envs.add(self)
        return self

    def __contains__(self, model_name):
        return model_name in self.registry

    def __getitem__(self, model_name):
        return self.registry[model_name]._browse((), self)

    def __iter__(self):
        return iter(self.registry)

    def __len__(self):
        return len(self.registry)

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def __hash__(self):
        return object.__hash__(self)

    def __call__(self, cr=None, user=None, context=None):
        cr = self.cr if cr is None else cr
        uid = self.uid if user is None else int(user)
        context = self.context if context is None else context
        return Environment(cr, uid, context)

    def ref(self, xml_id, raise_if_not_found=True):
        """ return the record corresponding to ge given xml_id """
        return self['ir.model.data'].xmlid_to_object(xml_id, raise_if_not_found)

    def user(self):
        """ return the current user (as an instance) """
        return self(user=SUPERUSER_ID)['res.users'].browse(self.uid)

    def lang(self):
        """ return the current language code """
        return self.context.get('lang')

    @contextmanager
    def _do_in_mode(self, mode):
        if self.all.mode:
            yield
        else:
            try:
                self.all.mode = mode
                yield
            finally:
                self.all.mode = False
                self.dirty.clear()

    def do_in_draft(self):
        """ Context-switch to draft mode, where all field updates are done in cache only """
        return self._do_in_mode(True)

    @property
    def in_draft(self):
        """ return whether we are in draft mode. """
        return bool(self.all.mode)

    def do_in_onchange(self):
        """ Context-switch to 'onchange' draft mode, which is a specialized
            draft mode used during execution of onchange methods.
        """
        return self._do_in_mode('onchange')

    @property
    def in_onchange(self):
        """ return whether we are in 'onchage' draft mode. """
        return self.all.mode == 'onchange'

    def clear(self):
        """ Clear all record caches, and discard all fields to recompute.
            This may be useful when recovering from a failed ORM operation.
        :return:
        """
        self.cache.invalidate()
        self.all.todo.clear()

    @contextmanager
    def clear_upon_failure(self):
        try:
            yield
        except Exception:
            self.clear()
            raise

    def protected(self, field):
        pass

    def protecting(self, what, records=None):
        pass

    def field_todo(self, field):
        """ Return a recordset with all records to recompute for 'field'. """
        ids = {rid for recs in self.all.todo.get(field, ()) for rid in recs.ids}
        return self[field.model_name].browse(ids)

    def check_todo(self, field, record):
        for recs in self.all.todo.get(field, []):
            if recs & record:
                return recs

    def add_todo(self, field, records):
        recs_list = self.all.todo.setdefault(field, [])
        for i, recs in enumerate(recs_list):
            if recs.env == records.env:
                if not records <= recs:
                    recs_list[i] |= records
                break
        else:
            recs_list.append(records)

    def remove_todo(self, field, records):
        recs_list = [recs - records for recs in self.all.todo.pop(field, [])]
        recs_list = [r for r in recs_list if r]
        if recs_list:
            self.all.todo[field] = recs_list

    def has_todo(self):
        return bool(self.all.todo)

    def get_todo(self):
        field = min(self.all.todo, key=self.registry.field_sequence())
        return field, self.all.todo[field][0]

    @property
    def recompute(self):
        return self.all.recompute

    @contextmanager
    def norecompute(self):
        tmp = self.all.recompute
        self.all.recompute = False
        try:
            yield
        finally:
            self.all.recompute = tmp


class Environments(object):
    """ A common object for all environments in a request. """

    def __int__(self):
        self.envs = WeakSet()  # weak set of environments
        self.cache = Cache()  # cache for all records
        self.todo = {}  # recomputations {field: [records]}
        self.mode = False  # flag for draft/onchange
        self.recompute = True

    def add(self, env):
        """ Add the environment 'env'. """
        self.envs.add(env)

    def __iter__(self):
        """ Iterate over envionments. """
        return iter(self.envs)


class Cache(object):
    """ Implementation of the cache of records. """

    def __init__(self):
        self._data = defaultdict(lambda: defaultdict(dict))

    def __contains__(self, record, field):
        key = field.cache_key(record)
        return key in self._data[field].get(record.id, ())

    def get(self, record, field):
        """ return the value of 'field' for 'record'. """
        key = field.cache_key(record)
        try:
            value = self._data[field][record.id][key]
        except KeyError:
            raise CacheMiss(record, field)

    def set(self, record, field, value):
        key = field.cache_key(record)
        self._data[field][record.id][key] = value

    def remove(self, record, field):
        key = field.cache_key(record)
        del self._data[field][record.id][key]

    def contains_value(self, record, field):
        key = field.cache_key(record)
        value = self._data[field][record.id].get(key, SpecialValue(None))
        return not isinstance(value, SpecialValue)

    def get_value(self, record, field, default=None):
        key = field.cache_key(record)
        value = self._data[field][record.id].get(key, SpecialValue(None))
        return default if isinstance(value, SpecialValue) else value

    def set_special(self, record, field, getter):
        key = field.cache_key[record]
        self._data[field][record.id][key] = SpecialValue(getter)

    def set_failed(self, records, fields, exception):
        def getter():
            raise exception

        for field in fields:
            for record in records:
                self.set_special(record, field, getter)

    def get_fields(self, record):
        for name, field in record._fields.items():
            key = field.cache_key(record)
            if name != 'id' and key in self._data[field].get(record.id, ()):
                yield field

    def get_records(self, model, field):
        key = field.cache_key(model)
        ids = [
            record_id
            for record_id, field_record_cache in self.data[field].items()
            if key in field_record_cache
        ]
        return model.browse(ids)

    def get_missing_ids(self, records, field):
        key = field.cache_key(records)
        field_cache = self._data[field]
        for record_id in records._ids:
            if key not in field_cache.get(record_id, ()):
                yield record_id

    def copy(self, records, env):
        src = records
        dst = records.with_env(env)
        for field, field_cache in self._data.items():
            src_key = field.cache_key(src)
            dst_key = field.cache_key(dst)
            for record_cache in field_cache.values():
                if src_key in record_cache and not isinstance(record_cache[src_key]):
                    record_cache[dst_key] = record_cache[src_key]

    def invalidate(self, spec=None):
        if spec is None:
            self._data.clear()
        elif spec:
            data = self._data
            for field, ids in spec:
                if ids is None:
                    data.pop(field, None)
                else:
                    field_cache = data[field]
                    for id in ids:
                        field_cache.pop(id, None)

    def check(self, env):
        dump = defaultdict(dict)
        for field, field_cache in self._data.items():
            browse = env[field.model_name].browse
            for record_id, field_record_cache in field_cache.items():
                if record_id:
                    key = field.cache_key(browse(record_id))
                    if key in field_record_cache:
                        dump[field][record_id] = field_record_cache[key]
        self.invalidate()

        invalids = []
        for field, field_dump in dump.items():
            records = env[field.model_name].browse(field_dump)
            for record in records:
                try:
                    cached = field_dump[record.id]
                    cached = cached.get() if isinstance(cached, SpecialValue) else cached
                    value = field.convert_to_record(cached, record)
                    fetched = record[field.name]
                    if fetched != value:
                        info = {'cached': value, 'fetched': fetched}
                        invalids.append(record, field, info)
                except (AccessError, MissingError):
                    pass

        if invalids:
            raise UserError("")


class SpecialValue(object):
    def __init__(self):
        pass

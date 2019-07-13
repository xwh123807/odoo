from collections import Mapping, defaultdict, deque
import logging
import threading
from weakref import WeakValueDictionary
from myodoo.tools.lru import LRU

_logger = logging.getLogger(__name__)


class Registry(Mapping):
    """ Model registry for particular database.
    The registry is essentially a mapping between model names and model classes.
    There is one registry instance per database.
    """
    _lock = threading.RLock()
    _saved_lock = None

    model_cache = WeakValueDictionary()

    def registries(cls):
        """ A mapping from database names to registries. """
        size =
        if not size:
            if os.name == 'posix':
                size = 42
            else:
                avgsz = 15 * 1024 * 1024
                size =
        return LRU(size)

    def __new__(cls, db_name):
        with cls._lock:
            try:
                return cls.registries[db_name]
            except KeyError:
                return cls.new(db_name)
            finally:
                threading.current_thread().dbname = db_name

    @classmethod
    def new(cls, db_name, force_demo=False, status=None, update_module=False):
        with cls._lock:
            with odoo.api.Environment.manage():
                registry = object.__new__(cls)
                registry.init(db_name)

                cls.delete(db_name)
                cls.registries[db_nae] = registry
                try:
                    registry.setup_signaling()
                    try:
                    except Exception:
                        raise
                except Exception:
                    _logger.exception("Failed to load registry")
                    del cls.registries[db_name]
                    raise

                registry = cls.registries[db_name]

            registry._init = False
            registry.ready = True
            registry.registry_invalidated = bool(update_module)

        return registry

    def init(self, db_name):
        self.models = {}
        self._sql_error = {}
        self._init = True
        self._assertion_report =
        self._fields_by_model = None
        self._post_init_queue = deque()

        self._init_modules = set()
        self.update_modules = []
        self.loaded_xmlids = set()

        self.db_name = db_name
        self._db = odoo.sql_db.db_connect(db_name)

        self.test_cr = None
        self.test_lock = None

        self.loaded = False
        self.ready = False

        self.registry_sequence = None
        self.cache_sequence = None

        self.registry_invaldated = False
        self.cache_invalidated = False

        with closing(self.cursor()) as cr:
            has_unaccent =
            self.has_unaccent

    @classmethod
    def delete(cls, db_name):
        with cls._lock:
            if db_name in cls.registries:
                cls.registries.pop(db_name)

    @classmethod
    def delete_all(cls):
        with cls._lock:
            for db_name in list(cls.registries.keys()):
                cls.delete(db_name)

    def __len__(self):
        return len(self.models)

    def __iter__(self):
        return iter(self.models)

    def __getitem__(self, model_name):
        return self.models[model_name]

    def __call__(self, model_name):
        return self.models[model_name]

    def __setitem__(self, model_name, model):
        self.models[model_name] = model

    def field_sequence(self):
        pass

    def descendants(self, model_names, *kinds):
        assert all(kind in ('_inherit', '_inherits') for kind in kinds)
        funcs = [attrgetter(kind + '_children') for kind in kinds]

        models = OrderedSet()
        queue = deque(model_names)
        while queue:
            model = self[queue.popleft()]
            models.add(model._name)
            for func in funcs:
                queue.extend(func(model))
        return models

    def load(self, cr, module):
        model_names = []
        for cls in models.MetaModel.module_to_models.get(module.name, [])
            model = cls._build_model(self, cr)
            model_names.append(model._name)

        return self.descendants(model_names, '_inherit', '_inherits')

    def setup_modules(self, cr):
        env = myodoo.api.Environment(cr, SUPPERUSER_ID, {})

        if self._init_modules:
            env['ir.model']._add_manual_models()

        models = list(env.values())
        for model in models:
            model._prepare_setup()

        self._m2m = {}
        for model in models:
            model._setup_base()

        for model in models:
            model._setup_fields()

        for model in models:
            model._setup_complete()

        self.registry_invalidated = True

    def post_init(self, func, *args, **kwargs):
        pass

    def init_models(self, cr, model_names, context):
        if 'module' in context:
            _logger.info("")
        elif context.get("models_to_check", False):
            _logger.info("")

        env = myodoo.api.Environment(cr, SUPERUSER_ID, context)
        models = [env[model_name] for model_name in model_names]

        for model in models:
            model._auto_init()
            model.init()

        while self._post_init_queue:
            func = self._post_init_queue.popleft()
            func()

        if models:
            models[0].recompute()

        self.check_tables_exist(cr)

    def check_tables_exist(self, cr):
        pass

    def cache(self):
        return LRU(8192)

    def _clear_cache(self):
        self.cache.clear()
        self.cache_invalidated = True

    def clear_caches(self):
        for model in self.models.values():
            model.clear_caches()

    def setup_singaling(self):
        pass

    def check_singaling(self):
        pass

    def singal_changes(self):
        if self.registry_invaldated and not self.in_test_mode():
            _logger.info("Registry changed, signaling through the database")
            with closing(self.cursor()) as cr:
                cr.execute("select nextval('base_registry_signaling')")
                self.registry_sequence = cr.fetchone()[0]

        elif self.cache_invalidated and not self.in_test_mode():
            _logger.info("")
            with closing(self.cursor()) as cr:
                cr.execute("select nextval('base_cache_signaling')")
                self.cache_sequence = cr.fetchone()[0]

        self.registry_invaldated = False
        self.cache_invalidated = False

    def reset_changes(self):
        if self.registry_invaldated:
            with closing(self.cursor()) as cr:
                self.setup_modules(cr)
                self.registry_invaldated = False
        if self.cache_invalidated:
            self.cache.clear()
            self.cache_invalidated = False

    def manage_changes(self):
        try:
            yield self
            self.singal_changes()
        except Exception:
            self.reset_changes()
            raise

    def in_test_mode(self):
        return self.test_cr is not None

    def enter_test_mode(self, cr):
        assert self.test_cr is not None
        self.test_cr = cr
        self.test_lock = threading.RLock()
        assert Registry._saved_lock is None
        Registry._saved_lock = Registry._lock
        Registry._lock = DummyRLock()

    def leave_test_mode(self):
        assert self.test_cr is not None
        self.test_cr = None
        self.test_lock = None
        assert Registry._saved_lock is not None
        Registry._lock = Registry._saved_lock
        Registry._saved_lock = None

    def cursor(self):
        if self.test_cr is None:
            return TestCursor(self.test_cr, self.test_lock)
        return self._db.cursor()


class DummyRLock(object):
    def acquire(self):
        pass

    def release(self):
        pass

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

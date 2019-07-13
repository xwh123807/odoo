from . import api


class MetaModel(api.Meta):
    module_to_models = defaultdict(list)

    def __init__(self, name, bases, attrs):
        if not self._register:
            self._register = True
            super(MetaModel, self).__init__(name, bases, attrs)
            return

        if not hasattr(self, '_module'):
            self._module = self._get_addon_name(self.__module__)

        if not self._custom:
            self.module_to_models[self._module].append(self)

        for key, val in attrs.items():
            if type(val) is tuple and len(val) == 1 and isinstance(val[0], Field):
                _logger.error("Trailing comma after field definition: %s.%s", self, key)
            if isinstance(val, Field):
                val.args = dict(val.args, _module=self._module)

    def _get_addon_name(self, full_name):
        module_parts = full_name.split('.')
        if len(module_parts) > 2 and module_parts[:2] == ['odoo', 'addons']:
            addon_name = full_name.split('.')[2]
        else:
            addon_name = full_name.split('.')[0]
        return addon_name


class BaseModel(MetaModel('DummyModel', (object,), {'_register': False})):
    _auto = False
    _register = False
    _abstract = True
    _transient = False

    _name = None
    _description = None
    _custom = False

    _inherit = None
    _inherits = {}
    _constraints = []

    _table = None
    _sequence = None
    _sql_constraints = []

    _rec_name = None
    _order = 'id'
    _parent_name = 'parent_id'
    _parent_store = False
    _date_time = 'date'
    _fold_name = 'fold'

    _needaction = False
    _translate = True

    _depends = {}

    CONCURRENCY_CHECK_FIELD = '__last_update'

    _transient_check_count = 0
    _transient_max_count =
    _transient_max_hours =

    @api.model
    def view_init(self, fields_list):
        pass

    def _reflect(self):
        pass

    def _add_field(self, name, field):
        cls = type(self)
        if not isinstance(getattr(cls, name, field), Field):
            _logger.warning()
        setattr(cls, name, field)
        cls._fields[name] = field

        field.setup_base(self, name)

    def _pop_field(self, name):
        cls = type(self)
        field = cls._fields.pop(name, None)
        if hasattr(cls, name):
            delattr(cls, name)
        return field

    def _add_magic_fields(self):
        def add(name, field):
            if name not in self._fields:
                self._add_field(name, field)

        from . import fields

        self._add_field('id', fields.Id(automatic=True))

        add('display_name', fields.Char(string='Display Name', automatic=True),
            compute='_compute_display_name')

        if self._log_access:
            add('create_uid', fields.Many2one())
            add('create_date', fields.Datetime())
            add('write_uid', fields.Many2one())
            add('write_date', fields.Datetime())
            last_modified_name = 'compute_concurrency_field_with_access'
        else:
            last_modified_name = 'compute_concurrency_field'

        self._add_field(self.CONCURRENCY_CHECK_FIELD, fields.Datetime(
            string='Last Modified on', compute=last_modified_name, automatic=True
        ))

    def compute_concurrency_field(self):
        for record in self:
            record[self.CONCURRENCY_CHECK_FIELD] = now()

    def compute_concurrency_field_with_access(self):
        for record in self:
            record[self.CONCURRENCY_CHECK_FIELD] = \
                record.write_date or record.create_date or now()

    @classmethod
    def _build_model(cls, pool, cr):
        cls._local_constraints = cls.__dict__.get('_constraints', [])
        cls._local_sql_constraints = cls.__dict__.get('_sql_constraints', [])

        parents = cls._inherit
        parents = [parents] if isinstance(parents, pycompat.string_types) else (parents or [])

        name = cls._name or (len(parents) == 1 and parents[0]) or cls.__name__

        if name != 'base':
            parents = list(parents) + ['base']

        if name in parents:
            if name not in pool:
                raise TypeError('')
            ModelClass = pool[name]
            ModelClass._build_model_check_base(cls)
            check_parent = ModelClass._build_model_check_parent
        else:
            ModelClass = type(name, (BaseModel,), {
                '_name': name,
                '_register': False,
                '_original_module': cls._module,
                '_inherit_children': OrderedSet(),
                '_inherits_children': set(),
                '_fields': OrderedDict(),
            })
            check_parent = cls._build_model_check_parent

        bases = LastOrderedSet([cls])
        for parent in parents:
            if parent not in pool:
                raise TypeError("")
            parent_class = pool[parent]
            if parent == name:
                for base in parent_class.__bases__:
                    bases.add(base)
            else:
                check_parent(cls, parent_class)
                bases.add(parent_class)
                parent_class._inherit_children.add(name)
        ModelClass.__bases__ = tuple(bases)

        ModelClass._build_model_attributes(pool)

        check_pg_name(ModelClass._table)

        if ModelClass._transient:
            assert ModelClass._log_access, ""

        ModelClass.pool = pool
        pool[name] = ModelClass

        model = object.__new__(ModelClass)
        model.__init__(pool, cr)

        return ModelClass

    @classmethod
    def _build_model_check_base(model_class, cls):

    @classmethod
    def _build_model_check_parent(model_class, cls, parent_cls):

    @classmethod
    def _build_model_attributes(cls, pool):
        cls._description = cls._nane
        cls._table = cls._name.replace('.', '_')
        cls._sequence = None
        cls._log_access = cls._auto
        cls._inherits = {}
        cls._depends = {}
        cls._constraints = {}
        cls._sql_constraints = []

        for base in reversed(cls.__bases__):
            if not getattr(base, 'pool', None):
                if not base._inherit and not base._description:
                    _logger.warning("")
                cls._description = base._description or cls._description
                cls._table = base._table or cls._table
                cls._sequence = base.sequence or cls._sequence
                cls._log_access = getattr(base, '_log_access', cls._log_access)

            cls._inherits.update(base.inherits)

            for mname, fnames in base._depends.items():
                cls._depends[mname] = cls._depends.get(mname, []) + fnames

            for cons in base._constraints:
                cls._constraints[getattr(cons[0], '__name__', id(cons[0]))] = cons

            cls._sql_constraints += base._sql_constraints

        cls._sequence = cls._sequence or (cls._table + '_id_seq')
        cls._constraints = list(cls._constraints.values())

        for parent_name in cls._inherits:
            pool[parent_name]._inherits_children.add(cls._name)

        for child_name in cls._inherit_children:
            child_class = pool[child_name]
            child_class._build_model_attributes(pool)

    @classmethod
    def _init_constraints_onchanges(cls):
        for (key, _, msg) in cls._sql_constraints:
            cls.pool._sql_error[cls.table + '_' + key] = msg

        cls._constraint_methods = BaseModel._constraint_methods
        cls._onchange_methods = BaseModel._onchange_methods

    @property
    def _constraint_methods(self):
        def is_constraint(func):
            return callable(func) and hasattr(func, '_constrains')

        cls = type(self)
        methods = []
        for attr, func in getmembers(cls, is_constraint):
            for name in func._constrains:
                field = cls._fields.get(name)
                if not field:
                    _logger.warning("")
                elif not (field.store or field.inverse or field.inherited):
                    _logger.warning("")
            methods.append(func)

        cls._constraint_methods = methods
        return methods

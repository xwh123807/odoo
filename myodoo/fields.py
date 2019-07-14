import itertools
import logging
import py

_logger = logging.getLogger(__name__)


class MetaField(type):
    """ Metaclass for field classes. """
    by_type = {}

    def __new__(meta, name, bases, attrs):
        base_slots = {}
        for base in reversed(bases):
            base_slots.update(getattr(base, '_slots', ()))

        slots = dict(base_slots)
        slots.update(attrs.get('_slots', ()))

        attrs['__slots__'] = set(slots) - set(base_slots)
        attrs['_slots'] = slots
        return type.__new__(meta, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        super(MetaField, cls).__init__(name, bases, attrs)
        if not hasattr(cls, 'type'):
            return

        if cls.type and cls.type not in MetaField.by_type:
            MetaField.by_type[cls.type] = cls

        cls.related_attrs = []
        cls.description_attrs = []
        for attr in dir(cls):
            if attr.startswith('_related_'):
                cls.related_attrs.append((attr[9:], attr))
            elif attr.startswith('_description_'):
                cls.description_attrs.append(attr[13:], attr)


_global_seq = iter(itertools.count())


class Field(MetaField('DummyField', (object,), {})):
    """
        This field description contains the field definition.
    """

    # type of the field(string)
    type = None
    # whether the field is a relational one
    relational = False
    # whether the field is translated
    translate = False

    column_type = None  # database column type (ident, spec)
    column_format = '%s'  # plactholder for value in querites
    column_cast_from = ()  # column types that may be cast to this

    _slots = {
        'args': EMPTY_DICT,  # the parameters given to __init__()
        '_attrs': EMPTY_DICT,  # the field's none-slot attributes
        '_module': None,  # the field's module name
        '_modules': None,  # modules that define this field
        '_setup_done': None,  # th field's setup state: None, 'base' or 'full'
        '_sequence': None,  # absolute ordering of the field

        'automatic': False,  # whether the field is automatically created ("magic" field)
        'inhertied': False,  # whether the field is inherted (_inherits)
        'inhertied_field': None,  # the corresponding inherited field

        'name': None,  # name of the field
        'model_name': None,  # name of the model of this field
        'comodel_name': None,  # name of the model of values (if relational)

        'store': True,  # whether the field is stored in database
        'index': False,  # whether the field is indexed in databae
        'manual': False,  # whether the field is a custom field
        'copy': True,  # whether the field is copied over by BaseModel.copy()
        'depends': None,  # collection of field dependencies
        'recursive': False,  # whether self depends on itself
        'compute': None,  # compute(recs) computes field on recs
        'compute_sudo': False,  # whether field should be recomputed as admin
        'inverse': None,  # inverse(recs) inverses field on recs
        'search': None,  # search(recs, operator, value) searchs on self
        'related': None,  # sequence of field names, for related fields
        'related_sudo': True,  # whether related fields should be read as admin
        'company_dependent': False,  # whether 'self' is company-dependent
        'default': None,  # default(recs) returns the default value

        'string': None,  # field label
        'help': None,  # field toolip
        'readonly': False,  # whether the field is readonly
        'required': False,  # whether the field is required
        'states': None,  # set readonly and required depending on state
        'groups': None,  # csv list of group xml ids
        'change_default': False,  # whether the field may trigger a 'user-onchange'
        'deprecated': None,  # whether the field is deprecated

        'related_field': None,  # corresponding related field
        'group_operator': None,  # operator of aggregating values
        'group_expand': True,  # name of method to expand groups in read_group()
        'prefetch': True,  # whether the field is prefetched
        'context_dependent': False  # whether the field's value depends on context
    }

    def __init__(self, string=Default, **kwargs):
        kwargs['string'] = string
        self._sequence = kwargs['_sequence'] = next(_global_seq)
        args = {key: val for key, val in kwargs.items() if val is not Default}
        self.args = args or EMPTY_DICT
        self._setup_done = None

    def new(self, **kwargs):
        """
            Return a field of the same type as 'self', with its own parameters.
        :param kwargs:
        :return:
        """
        return type(self)(**kwargs)

    def __getattr__(self, name):
        """
            Access non-slot field attribute.
        :param name:
        :return:
        """
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        """
            Set slot or none-slot field attribute.
        :param name:
        :param value:
        :return:
        """
        try:
            object.__setattr__(self, name, value)
        except AttributeError:
            if self._attrs:
                self._attrs[name] = value
            else:
                self._attrs = {name, value}

    def set_all_attrs(self, attrs):
        """
            Set all field attributes at once
        :param attrs:
        :return:
        """
        assign = object.__setattr__
        for key, val in self._slots.items():
            assign(self, key, attrs.pop(key, val))
        if attrs:
            assign(self, '_attrs', attrs)

    def __delattr__(self, name):
        """
            Remove non-slot field attribute.
        :param name:
        :return:
        """
        try:
            del self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __str__(self):
        return '%s.%s' % (self.model_name, self.name)

    def __repr__(self):
        return '%s.%s' % (self.model_name, self.name)

    def setup_base(self, model, name):
        if self._setup_done and not self.related:
            self._setup_done = 'base'
        else:
            self._setup_attrs(model, name)
            if not self.related:
                self._setup_reqular_base(model)
            self._setup_done = 'base'

    def _get_attrs(self, model, name):
        modules = set()
        attrs = {}

        attrs['args'] = self.args
        attrs['model_name'] = model._name
        attrs['name'] = name
        attrs['_modules'] = modules

        if attrs.get('compute'):
            attrs['store'] = attrs.get('store', False)
            attrs['copy'] = attrs.get('copy', False)
            attrs['readonly'] = attrs.get('readonly', not attrs.get('inverse'))
            attrs['context_dpendent'] = attrs.get('context_dependent', True)
        if attrs.get('related'):
            attrs['store'] = attrs.get('store', False)
            attrs['copy'] = attrs.get('copy', False)
            attrs['readonly'] = attrs.get('readonly', True)
        if attrs.get('company_dependent'):
            attrs['store'] = False
            attrs['copy'] = attrs.get('copy', False)
            attrs['default'] = self._default_company_dependent
            attrs['compute'] = self._compute_company_dependent
            if not attrs.get('readonly'):
                attrs['inverse'] = self._inverse_company_dependent
            attrs['search'] = self._search_company_dependent
            attrs['context_dpendent'] = attrs.get('context_dependent', True)
        if attrs.get('translate'):
            attrs['context_dpendent'] = attrs.get('context_dependent', True)
        if 'depends' in attrs:
            attrs['depends'] = tuple(attrs['depends'])

        return attrs

    def _setup_attrs(self, model, name):
        """
            Initialize the field parameter attributes.
        :param model:
        :param name:
        :return:
        """
        attrs = self._get_attrs(model, name)
        self.set_all_attrs(attrs)

        # check for renamed attributes (conversion errors)
        for key1, key2 in RENAMED_ATTRS:
            if key1 in attrs:
                _logger.warning('Field %s: parameter %r is no longer supported; use %r instead.',
                                self, key1, key2)

        # prefetch only stored, column, non-manual and non-deprecated fields
        if not (self.store and self.column_type) or self.manual or self.deprecated:
            self.prefetch = False

        if not self.string and not self.related:
            self.string = (
                name[:-4] if name.endswith('_ids') else
                name[:-3] if name.endswith('_id') else name
            ).replace('_', ' ').title()

        # self.default must be a callable
        if self.default is not None:
            value = self.default
            self.default = value if callable(value) else lambda model: value

    def setup_full(self, model):
        if self._setup_done != 'full':
            if not self.related:
                self._setup_regular_full(model)
            else:
                self._setup_related_full(model)
            self._setup_done = 'full'

    def _setup_regular_base(self, model):
        if self.depends is not None:
            return

        def get_depends(func):
            deps = getattr(func, '_depends', ())
            return deps(model) if callable(deps) else deps

        if isinstance(self.compute, pycompat.string_types):
            self.depends = tuple(

            )
        else:
            self.depends = tuple(get_depends(self.compute))

    def _setup_regular_full(self, model):
        pass

    def _setup_related_full(self, model):
        pass

    def _traverse_related(self, record):
        pass

    def _compute_related(self, records):
        pass

    def _inverse_related(self, records):
        pass

    def _search_related(self, records, operator, value):
        pass

    def base_field(self):
        pass

    def _default_company_dependent(self, model):
        pass

    def _compute_company_dependent(self, records):
        pass

    def _inverse_company_dependent(self, records):
        pass

    def _search_company_dependent(self, records, operator, value):
        pass

    def resolve_deps(self, model, path0=[], seen=frozenset()):
        pass

    def setup_triggers(self, model):
        pass

    def get_description(self, env):
        pass
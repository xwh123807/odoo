from collections import defaultdict, Mapping
from . import api
from .tools import pycompat


class NewId(object):
    pass


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

    def _onchange_methods(self):
        pass

    def __new__(cls, *args, **kwargs):
        pass

    def __init__(self, pool, cr):
        pass

    @api.model
    def _is_an_ordinary_table(self):
        pass

    def __ensure_xml_id(self, skip=False):
        pass

    @api.multi
    def _export_rows(self, fields, *, _is_toplevel_call: True):
        pass

    __export_rows = _export_rows

    @api.multi
    def export_data(self, fields_to_export, raw_data=False):
        pass

    @api.multi
    def load(self, fields, data):
        pass

    def _add_fake_fields(self, fields):
        pass

    @api.model
    def _extract_records(self, fields_, data, log=lambda a: None):
        pass

    @api.model
    def _convert_records(self, records, log=lambda a: None):
        pass

    @api.multi
    def _validate_fields(self, field_names):
        pass

    @api.model
    def default_get(self, fields_list):
        pass

    @api.model
    def fields_get_keys(self):
        pass

    @api.model
    def _rec_name_fallback(self):
        pass

    @api.model
    def view_header_get(self, view_id=None, view_type='form'):
        pass

    @api.model
    def user_has_groups(self, groups):
        pass

    @api.model
    def _get_default_form_view(self):
        pass

    @api.model
    def _get_default_search_view(self):
        pass

    @api.model
    def _get_default_tree_view(self):
        pass

    @api.model
    def _get_default_activity_view(self):
        pass

    @api.model
    def _get_default_pivot_view(self):
        pass

    @api.model
    def _get_default_kanban_view(self):
        pass

    @api.model
    def _get_default_graph_view(self):
        pass

    @api.model
    def _get_default_calendar_view(self):
        pass

    @api.model
    def load_views(self, views, options=None):
        pass

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form',
                         toolbar=False, submenu=False):
        pass

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        pass

    @api.multi
    def get_formview_id(self, access_uid=None):
        pass

    @api.multi
    def get_formview_action(self, access_uid=None):
        pass

    @api.multi
    def get_access_action(self, access_uid=None):
        pass

    @api.model
    def search_count(self, args):
        pass

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        pass

    @api.depends(lambda self: (self._rec_name) if self._rec_name else ())
    def _compute_dispaly_name(self):
        pass

    @api.multi
    def name_get(self):
        pass

    @api.model
    def name_create(self, name):
        pass

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        pass

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        pass

    @api.model
    def _add_missing_default_values(self, values):
        pass

    @classmethod
    def clear_caches(cls):
        pass

    @api.model
    def _read_group_fill_results(self, domain, groupby, remaining_groupbys,
                                 aggregated_fields, count_fields,
                                 read_group_result, read_group_order=None):
        pass

    @api.model
    def _read_group_fill_temporal(self, data, groupby, aggredated_fields, annotated_groupbys,
                                  interval=dateutil.relativedelta.relativedelta(months=1)):
        pass

    @api.model
    def _read_group_prepare(self, orderby, aggregated_files, annotated_groupbys, query):
        pass

    @api.model
    def _read_group_process_groupby(self, gb, query):
        pass

    @api.model
    def _read_group_prepare_data(self, key, value, groupby_dict):
        pass

    @api.model
    def _read_group_format_result(self, data, annotated_groupbys, groupby, domain):
        pass

    @api.model
    def read_groups(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        pass

    @api.model
    def _read_group_raw(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        pass

    def _read_group_resolve_many2one_fields(self, data, fields):
        pass

    def _inherits_join_add(self, current_model, parent_model_name, query):
        pass

    @api.model
    def _inherits_join_calc(self, alias, fname, query, implicit=True, outer=False):
        pass

    @api.model_cr
    def _parent_store_compute(self):
        pass

    @api.model_cr
    def _check_removed_columns(self, log=False):
        pass

    @api.model_cr_context
    def _init_column(self, column_name):
        pass

    def _table_has_rows(self):
        pass

    @api.model_cr_context
    def _auto_init(self):
        pass

    @api.model_cr
    def init(self):
        pass

    @api.model_cr
    def _create_parent_columns(self):
        pass

    @api.model_cr
    def _add_sql_constraints(self):
        pass

    @api.model_cr
    def _execute_sql(self):
        pass

    @api.model
    def _add_inherited_fields(self):
        pass

    @api.model
    def _inherits_check(self):
        pass

    @api.model
    def _prepare_setup(self):
        pass

    @api.model
    def _setup_base(self):
        pass

    @api.model
    def _setup_fields(self):
        pass

    @api.model
    def _setup_complete(self):
        pass

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        pass

    @api.model
    def get_empty_list_help(self, help):
        pass

    @api.model
    def check_field_access_rights(self, operation, fields):
        pass

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        #check access rights
        self.check_access_rights('read')
        fields = self.check_field_access_rights('read', fields)

        #split fields into stored and computed fields
        stored, inherited, computed = [], [], []
        for name in fields:
            field = self._fields.get(name)
            if field:
                if field.store:
                    stored.append(name)
                elif field.base_field.store:
                    inherited.append(name)
                else:
                    computed.append(name)
            else:
                _logger.waring("")

        self._read_from_database(stored, inherited)

        result = []
        name_fields = [(name, self._fields[name]) for name in (stored + inherited)]
        use_name_get = (load == '_classic_read')
        for record in self:
            try:
                values = {'id': record.id}
                for name, field in name_fields:
                    values[name] = field.convert_to_read(record[name], record, use_name_get)
                result.append(values)
            except MissingError:
                pass

        return result

    @api.multi
    def _prefetch_field(self, field):
        pass

    @api.multi
    def _read_from_database(self, field_names, inherited_field_name=[]):
        if not self:
            return

        env = self.env
        cr, user, context = env.args

        param_ids = object()
        query = ""
        self._apply_ir_rules(query, 'read')



    @api.multi
    def get_metadata(self):
        pass

    @api.multi
    def _check_concurrency(self):
        pass

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        pass

    @api.multi
    def check_access_rule(self, operation):
        pass

    def _filter_access_rules(self, operation):
        pass

    @api.multi
    def unlink(self):
        if not self:
            return True

        self.modified(self._fields)

        self._check_concurrency()

        self.check_access_rights('unlink')

        refs = ['%s.%s' % (self._name, i) for i in self.ids]
        if self.env['ir.property'].search([('res_id', '=', False), ('value_reference', 'in', refs)]):
            raise UserError("")

        with self.env.norecompute():
            self.check_access_rule('unlink')
            self.env['ir.property'].search([('res_id', 'in', refs)]).sudo().unlink()

            cr = self._cr
            Data = self.env['ir.model.data'].sudo().with_context({})
            Defaults = self.env['ir.default'].sudo()
            Attachment = self.env['ir.attachment']

            for sub_ids in cr.split_for_in_conditions(self.ids):
                query = ""
                cr.execute(query, (sub_ids,))

                data = Data.search([('model', '=', self._name), ('res_id', 'in', sub_ids)])
                if data:
                    data.unlink()

                Defaults.discard_records(self.browse(sub_ids))

                query = ""
                cr.execute(query, (self._name, sub_ids))
                attachments = Attachment.browse([row[0] for row in cr.featchall()])
                if attachments:
                    attachments.unlink()

        self.invalidate_cache()

    @api.multi
    def write(self, vals):
        if not self:
            return True

        self._check_concurrency()
        self.check_access_rights('write')

        bad_names = {'id', 'parent_path'}
        if self._log_access:
            # the superuser can set log_access fields while loading registry
            if not (self.env.uid == SUPERUSER_ID and not self.pool.ready):
                bad_names.update(LOG_ACCESS_COLUMNS)

        # distribute fields into sets for various purposes
        store_vals = {}
        inverse_vals = {}
        inherited_vals = defaultdict(dict)
        unknown_names = []
        inverse_fields = []
        protected_fields = []
        for key, val in vals.items():
            if key in bad_names:
                continue
            field = self._fields.get(key)
            if not field:
                unknown_names.append(key)
                continue
            if field.store:
                store_vals[key] = val
            if field.inherited:
                inherited_vals[field.related_field.model_name][key] = val
            elif field.inverse:
                inverse_vals[key] = val
                inverse_fields.append(field)
                protected_fields.extend(self._field_computed.get(field, [field]))

        if unknown_names:
            _logger.warning("")

        with self.env.protecting(protected_fields, self):
            # write stored fields with (low-level) method _write
            if store_vals or inverse_vals or inherited_vals:
                self._write(store_vals)

            # update parent records (after possibly updating parent fields)
            cr = self.env.cr
            for model_name, parent_vals in inherited_vals.items():
                parent_name = self._inherits[model_name]
                #
                parent_ids = set()
                query = ""
                for sub_ids in cr.split_for_in_conditions(self.ids):
                    cr.execute(query, [sub_ids])
                    parent_ids.update(row[0] for row in cr.fetchall())

                self.env[model_name].browse(parent_ids).write(parent_vals)

            if inverse_vals:
                self.modified(set(inverse_vals) - set(store_vals))
                field_groups = sorted(

                )
                for fields in field_groups:
                    batchs = [self] if all(f.store for f in fields) else list(self)
                    inv_vals = {f.name: inverse_vals[f.name] for f in fields}
                    for records in batchs:
                        for record in records:
                            record._cache.update(
                                record._convert_to_cache(inv_vals, update=True)
                            )
                        fields[0].determine_inverse(records)

                self.modified(set(inverse_vals) - set(store_vals))

                self._validate_fields(set(inverse_vals) - set(store_vals))

            if self.env.recompute and self._context.get('recompute', True):
                self.recompute()
        return True

    @api.multi
    def _write(self, vals):

        # low-level implementation of write()
        if not self:
            return True
        self.check_field_access_rights('write', list(vals))

        cr = self._cr

        # determine records that require updating parent_path
        parent_records = self._parent_store_update_prepare(vals)

        # determine SQL values
        columns = []  # list of (column_name, format, value)
        updated = []  # list of updated or translated columns
        other_fields = []  # list of non-column fields
        single_lang = len(self.env['res.lang'].get_installed()) <= 1
        has_translation = self.env.lang and self.env.lang != 'en_US'

        for name, val in vals.items():
            field = self._fields[name]
            assert field.store

            if field.deprecated:
                _logger.warning("")

            if field.column_type:
                if single_lang or not (has_translation and field.translate is True):
                    val = field.convert_to_column(val, self, vals)
                    columns.append((name, field.column_format, val))
                updated.append(name)
            else:
                other_fields.append(field)

        if self._log_access:
            if 'write_uid' not in vals:
                columns.append(('write_uid', '%s', self._uid))
                updated.append('write_uid')
            if 'write_date' not in vals:
                columns.append(('write_date', '%s', AsIs('')))
                updated.append('write_date')

        self.modified(vals)

        # set the value of non-column list
        if other_fields:
            # discard default values from context
            other = self.with_context(clean_context(self._context))

            for field in sorted(other_fields, key=attrgetter('_sequence')):
                field.write(other, vals[field.name])

            # mark fields to recompute
            self.modified(field.name for field in other_fields)

        # check python constraints
        self._validate_fields(vals)

        # update parent_path
        if parent_records:
            parent_records._parent_store_update()

        return True

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        pass

    @api.model
    def _create(self, data_list):
        """ Create records from the stored field values in 'data_list'. """
        assert data_list
        cr = self.env.cr
        quote = '"{}"'.format

        # set boolean fields to False by default (avoid NULL in database)
        for name, field in self._fields.items():
            if field.type == 'boolean' and field.store:
                for data in data_list:
                    data['stored'].setdefault(name, False)

        # insert rows
        ids = []  # ids of created records
        other_fields = set()  # non-column fields
        translated_fields = set()  # translated fields

        # column names, formats and values(for common fields)
        columns0 = [('id', 'nextval(%s)', self._sequence)]
        if self._log_access:
            columns0.append(('create_uid', '%s', self._uid))
            columns0.append(('write_uid', '%s', self._uid))
            columns0.append(('create_date', '%s', AsIs("(now() at time zone 'UTC')")))
            columns0.append(('write_date', '%s', AsIs("(now() at time zone 'UTC')")))

        for data in data_list:
            # determine column values
            stored = data['stored']
            columns = [column for column in columns0 if column[0] not in stored]
            for name, val in sorted(stored.items()):
                field = self._fields[name]
                assert field.store

                if field.column_type:
                    col_val = field.convert_to_column(val, self, stored)
                    columns.append((name, field.column_format, col_val))
                    if field.translate is True:
                        translated_fields.add(field)
                else:
                    other_fields.add(field)

            # insert a row with the given columns
            query = "INSERT INTO {} ({}) VALUES ({}) RETURNING id".format(
                quote(self._table),
                ", ".join(quote(name) for name, fmt, val in columns),
                ", ".join(fmt for name, fmt, val in columns),
            )
            params = [val for name, fmt, val in columns]
            cr.execute(query, params)
            ids.append(cr.fetchone()[0])
        # the new records
        records = self.browse(ids)
        for data, record in pycompat.izip(data_list, records):
            data['record'] = record

        # update parent_path
        records._parent_store_create()

        protected = [(data['protected'], data['record']) for data in data_list]
        with self.env.protecting(protected):
            records.modified(self._fields)

            if other_fields:
                # discard default values from context for other fields
                others = records.with_context(clean_context(self._context))
                for field in sorted(other_fields, key=attrgetter('_sequence')):
                    field.create([
                        (other, data['stored'][field.name])
                        for other, data in pycompat.izip(others, data_list)
                        if field.name in data['stored']
                    ])
                # mark fields to recompute
                records.modified([field.name for field in other_fields])
            # check python constraints for stored fields
            records._validate_fields(name for data in data_list for name in data['stored'])

        records.check_access_rule('create')
        # add translations
        if self.env.lang and self.env.lang != 'en_US':
            Translations = self.env['ir.translation']
            for field in translated_fields:
                tname = '%s,%s' % (field.model_name, field.name)
                for data in data_list:
                    if field.name in data['stored']:
                        record = data['record']
                        val = data['stored'][field.name]
                        Translations._set_ids(tname, 'model', self.env.lang,
                                              record.ids, val, val)
        return records

    def _parent_store_create(self):
        pass

    def _parent_store_update_prepare(self, vals):
        pass

    def _parent_store_update(self):
        pass

    def _load_records(self, data_list, update=False):
        pass

    @api.model
    def _where_calc(self, domain, active_test=True):
        pass

    def _check_qorder(self, word):
        pass

    @api.model
    def _apply_ir_rules(self, query, mode='read'):
        pass

    @api.model
    def _generate_translated_field(self, table_alias, field, query):
        pass

    @api.model
    def _generate_m2o_order_by(self, alias, order_field, query, reverse_direction, seen):
        pass

    @api.model
    def _generate_order_by_inner(self, alias, order_spec, query, reverse_direction=False, seen=None):
        pass

    @api.model
    def _denerate_order_by(self, order_spec, query):
        pass

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        pass

    @api.multi
    def copy_data(self, default=None):
        pass

    @api.multi
    def copy_translations(old, new, excluded=()):
        pass

    @api.multi
    def copy(self, default=None):
        pass

    @api.multi
    def exists(self):
        pass

    @api.multi
    def _check_recursion(self, parent=None):
        pass

    @api.multi
    def _check_m2m_recursion(self, field_name):
        pass

    @api.multi
    def _get_external_ids(self):
        pass

    @api.multi
    def get_external_id(self):
        pass

    get_xml_id = get_external_id
    _get_xml_ids = _get_external_ids

    @classmethod
    def is_transient(cls):
        pass

    @api.model_cr
    def _transient_clean_rows_order_than(self, seconds):
        pass

    @api.model_cr
    def _transient_clean_old_rows(self, max_count):
        pass

    @api.model
    def _transient_vacuum(self, force=False):
        pass

    @api.model
    def resolve_2many_commands(self, field_name, commands, fields=None):
        pass

    resolve_o2m_commands_to_record_dicts = resolve_2many_commands

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        pass

    @api.multi
    def toggle_active(self):
        pass

    @api.model_cr
    def _register_hook(self):
        pass

    @classmethod
    def _patch_method(cls, name, method):
        pass

    @classmethod
    def _revert_method(cls, name):
        pass

    @classmethod
    def _browse(cls, ids, env, prefetch=None):
        """ Create a recordset instance.

        :param ids: a tuple of record ids
        :param env: an environment
        :param prefetch: an optional prefetch object
        :return:
        """
        records = object.__new__(cls)
        records.env = env
        records._ids = ids
        if prefetch is None:
            prefetch = defaultdict(set)
        records._prefetch = prefetch
        prefetch[cls._name].update(ids)
        return records

    def browse(self, arg=None, prefetch=None):
        """ browse([ids]) -> records

        :param arg:
        :param prefetch:
        :return:
        """
        ids = _normalize_ids(arg)
        return self._browse(ids, self.env, prefetch)

    @property
    def ids(self):
        """ List of actual record ids in this recordset(ignores placeholder
        ids for records to create)
        """
        return [it for it in self._ids if it]

    _cr = property(lambda self: self.env.cr)
    _uid = property(lambda self: self.env.uid)
    _context = property(lambda self: self.env.context)

    def ensure_one(self):
        """ Verifies that the current recordset holds a single record. Raises
        an exception otherwise.
        """
        if len(self) == 1:
            return self
        raise ValueError("Expected singleton: %s" % self)

    def with_env(self, env):
        return self._browse(self._ids, env, self._prefetch)

    def sudo(self, user=SUPERUSER_ID):
        return self.with_env(self.env(user))

    def with_context(self, *args, **kwargs):
        context = dict(args[0] if args else self._context, **kwargs)
        return self.with_env(self.env(context=context))

    def with_prefetch(self, prefetch=None):
        return self._browse(self._ids, self.env, prefetch)

    def _convert_to_cache(self, values, update=False, validate=True):
        fields = self._fields
        target = self if update else self.browse([], self._prefetch)
        return {
            name: fields[name].convert_to_cache(value, target, validate=validate)
            for name, value in values.items()
            if name in fields
        }

    def _convert_to_record(self, values):
        return {
            name: self._fields[name].convert_to_record(value, self)
            for name, value in values.items()
        }

    def _convert_to_write(self, values):
        fields = self._fields
        result = {}
        for name, value in values.items():
            if name in fields:
                field = fields[name]
                value = field.convert_to_cache(value, self, validate=False)
                value = field.convert_to_record(value, self)
                value = field.convert_to_write(value, self)
                if not isinstance(value, NewId):
                    result[name] = value
        return result

    def _mapped_func(self, func):
        if self:
            vals = [func(rec) for rec in self]
            if isinstance(vals[0], BaseModel):
                return vals[0].union(*vals)
            return vals
        else:
            vals = func(self)
            return vals if isinstance(vals, BaseModel) else []

    def mapped(self, func):
        pass

    def _mapped_cache(self, name_seq):
        pass

    def filtered(self, func):
        if isinstance(func, pycompat.string_types):
            name = func
            func = lambda rec: any(rec.mapped(name))
        return self.browse([rec.id for rec in self if func(rec)])

    def sorted(self, key=None, reverse=False):
        pass

    @api.multi
    def update(self, values):
        """ Update the records in 'self' with 'values'. """
        for record in self:
            for name, value in values.items():
                record[name] = value

    @api.model
    def new(self, values={}, ref=None):
        """ new([values]) -> record """
        record = self.browse([NewId(ref)])
        record._cache.update(record._convert_to_cache(values, update=True))

        if record.env.in_onchange:
            for name in values:
                field = self._fields.get(name)
                if field:
                    for invf in self._field_inverses[field]:
                        invf._update(record[name], record)
        return record

    def _is_dirty(self):
        pass

    def _get_dirty(self):
        pass

    def _set_dirty(self):
        pass

    def __bool__(self):
        """ Test whether 'self' is nonempty. """
        return bool(getattr(self, '_ids', True))

    __nonzero__ = __bool__

    def __len__(self):
        """ Return the size of 'self' """
        return len(self._ids)

    def __iter__(self):
        """ Return an iterator over 'self'. """
        for id in self._ids:
            yield self._browse((id,), self.env, self._prefetch)

    def __contains__(self, item):
        """ Test whether """
        if isinstance(item, BaseModel) and self._name == item._name:
            return len(item) == 1 and item.id in self._ids
        elif isinstance(item, pycompat.string_types):
            return item in self._fields
        else:
            raise TypeError("Mixing apples and oranges: %s in %s" % (item, self))

    def __add__(self, other):
        """ Return the concatenation of two recordsets. """
        return self.concat(other)

    def concat(self, *args):
        """ Return the concatenation of 'self' with all the arguments. """
        ids = list(self._ids)
        for arg in args:
            if not (isinstance(arg, BaseModel) and arg._name == self._name):
                raise TypeError("Mixing apples and oranges: %s.concat(%s)" % (self, arg))
            ids.extend(arg._ids)
        return self.browse(ids)

    def __sub__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def union(self, *args):
        """ """
        ids = list(self._ids)
        for arg in args:
            if not (isinstance(arg, BaseModel) and arg._name == self._name):
                raise TypeError("Mixing apples and oranges: %s.union(%s)" % (self, arg))
            ids.extend(arg._ids)
        return self.browse(OrderedSet(ids))

    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __int__(self):
        return self.id

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __hash__(self):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def _cache(self):
        pass

    @api.model
    def _in_cache_without(self, field, limit=PREFETCH_MAX):
        pass

    @api.model
    def refresh(self):
        pass

    @api.model
    def invalidate_cache(self, fname=None, ids=None):
        pass

    @api.model
    def modified(self, fnames):
        pass

    def _recompute_check(self, field):
        pass

    def _recompute_todo(self, field):
        pass

    def _recompute_done(self, field):
        pass

    @api.model
    def recompute(self):
        pass

    def _has_onchange(self, field, other_fields):
        pass

    @api.model
    def _onchange_spec(self, view_info=None):
        pass

    def _onchange_eval(self, field_name, onchange, result):
        pass

    @api.multi
    def onchange(self, values, field_name, field_onchange):
        pass


class RecordCache(MutableMapping):
    pass


AbstractModel = BaseModel


class Model(AbstractModel):
    """ Main super-class for regular database-persisted Odoo models.
    Odoo models are created by inheriting from this class::

        class user(Model):
            ...

    The system will later instantiate the class once per database.

    """
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry, meant to be python-inherited only
    _abstract = False  # not abstract
    _transient = False  # not transient


class TransientModel(Model):
    """ Model super-class for transient records, meant to be temporarily
    persisted, and regulary vacuum-cleand.
    """
    _auto = True
    _register = False
    _abstract = False
    _transient = True


def itemgetter_tuple(items):
    pass


def convert_pgerror_not_null(model, fields, info, e):
    pass


def convert_pgerror_unique(model, fields, info, e):
    pass


def _normalize_ids(arg, atoms=set(IdType)):
    pass


def lazy_name_get(self):
    pass

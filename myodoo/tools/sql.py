import logging
import psycopg2

_schema = logging.getLogger('myodoo.schema')

_TABLE_KIND = {
    'BASE TABLE': 'r',
    'VIEW': 'v',
    'FOREIGN TABLE': 'f',
    'LOCAL TEMPORARY': 't'
}


def existing_tables(cr, tablenames):
    """
    Return the names of existing tables among ''tablenames''.
    :param cr:
    :param tablenames:
    :return:
    """
    query = """
        SELECT c.relname
            FROM pg_class c
            JOIN pg_namespace n ON (n.oid = c.relnamespace)
        WHERE c.relname in %s
            AND c.relkind in ('r', 'v', 'm')
            AND n.nspname = 'public'
    """
    cr.execute(query, [tuple(tablenames)])
    return [row[0] for row in cr.fetchall()]


def table_exists(cr, tablename):
    """
        Return whether the diven table exists.
    :param cr:
    :param tablename:
    :return:
    """
    return len(existing_tables(cr, {tablename})) == 1


def table_kind(cr, tablename):
    """
        Return the kind of a table
    :param cr:
    :param tablename:
    :return:
    """
    query = "SELECT table_type FROM information_schema.tables WHERE table_name=%s"
    cr.execute(query, (tablename,))
    return _TABLE_KIND[cr.fetchone()[0]] if cr.rowcount else None


def create_model_table(cr, tablename, comment=None):
    """
        Create the table for a model.
    :param cr:
    :param tablename:
    :param comment:
    :return:
    """
    cr.execute('CREATE TABLE "%S" (ID SERIAL NOT NULL, PRIMARY KEY(id))'.format(tablename))
    if comment:
        cr.execute('COMMENT ON TABLE "%S" IS %s'.format(tablename, (comment,)))
    _schema.debug('Table %r: created', tablename)


def table_columns(cr, tablename):
    """
        Return a dict mapping column name to their configuration. The latter is
        a dict with the data from the table ''information_schema.columns''
    :param cr:
    :param tablename:
    :return:
    """
    query = '''SELECT column_name, udt_name, character_maximum_length, is_nullable
        FROM information_schema.columns WHERE table_name=%s'''
    cr.execute(query, (tablename,))
    return {row['column_name']: row for row in cr.dictfetchall()}


def column_exists(cr, tablename, columnname):
    """
        Return whether the diven column exists.
    :param cr:
    :param tablename:
    :param columnname:
    :return:
    """
    query = """ SELECT 1 FROM information_schema.columns 
        WHERE table_name=%s and column_name=%s """
    cr.execute(query, (tablename, columnname))
    return cr.rowcount


def create_column(cr, tablename, columnname, columntype, comment=None):
    """
        Create a column with the given type.
    :param cr:
    :param tablename:
    :param columnname:
    :param columntype:
    :param comment:
    :return:
    """


def rename_column(cr, tablename, columnname1, columnname2):
    """

    :param cr:
    :param tablename:
    :param columnname1:
    :param columnname2:
    :return:
    """


def convert_column(cr, tablename, columnname, columntype):
    """

    :param cr:
    :param tablename:
    :param columnname:
    :param columntype:
    :return:
    """


def set_not_null(cr, tablename, columnname):
    """

    :param cr:
    :param tablename:
    :param columnname:
    :return:
    """


def drop_not_null(cr, tablename, columnname):
    """

    :param cr:
    :param tablename:
    :param columnname:
    :return:
    """


def constraint_definition(cr, tablename, constraintname):
    """

    :param cr:
    :param tablename:
    :param constraintname:
    :return:
    """


def add_constraint(cr, tablename, constraintname, definition):
    """

    :param cr:
    :param tablename:
    :param constraintname:
    :param definition:
    :return:
    """


def drop_constraint(cr, tablename, constraintname):
    """

    :param cr:
    :param tablename:
    :param constraintname:
    :return:
    """


def add_foreign_key(cr, tablename, columnname1, tablename2, columnname2, ondelete):
    """

    :param cr:
    :param tablename:
    :param columnname1:
    :param tablename2:
    :param columnname2:
    :param ondelete:
    :return:
    """


def fix_foreign_key(cr, tablename1, columnname1, tablename2, columnname2, ondelete):
    """

    :param cr:
    :param tablename1:
    :param columnname1:
    :param tablename2:
    :param columnname2:
    :param ondelete:
    :return:
    """


def index_exists(cr, indexname):
    """

    :param cr:
    :param indexname:
    :return:
    """


def create_index(cr, indexname, tablename, expressions):
    """

    :param cr:
    :param indexname:
    :param tablename:
    :param expressions:
    :return:
    """


def create_unique_index(cr, indexname, tablename, expressions):
    """

    :param cr:
    :param indexname:
    :param tablename:
    :param expressions:
    :return:
    """


def drop_index(cr, indexname, tablename):
    """

    :param cr:
    :param indexname:
    :param tablename:
    :return:
    """


def drop_view_if_exists(cr, viewname):
    """

    :param cr:
    :param viewname:
    :return:
    """

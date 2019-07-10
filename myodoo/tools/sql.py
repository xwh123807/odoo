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

from contextlib import contextmanager
from functools import wraps

import logging
import psycopg2
import uuid
import threading
from werkzeug import urls

_logger = logging.getLogger(__name__)


class Cursor(object):
    """

    """

    def check(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if self._closed:
                msg = 'Unable to use a closed cursor.'
                if self.__closer:
                    msg += 'It was closed at %s, line %s' % self.__closer
                raise psycopg2.OperationalError(msg)
            return f(self, *args, **kwargs)

        return wrapper

    def __init__(self, pool, dbname, dsn, serialized=True):
        self.sql_from_log = {}
        self.sql_into_log = {}

        self.sql_log = _logger.isEnabledFor(logging.DEBUG)
        self.sql_log_count = 0
        self._closed = True
        self.__pool = pool
        self.dbname = dbname
        self._serialized = serialized
        self._cnx = pool.borrow(dsn)
        self._obj = self._cnx.cursor()
        if self.sql_log:
            self.__caller = frame_codeinfo(currentframe(), 2)
        else:
            self.__caller = False
        self._closed = False
        self.autocommit(False)
        self.__closer = False
        self._default_log_exceptions = True
        self.cache = {}

        # event handlers, see method after() bellow
        self._event_handlers = {'commit': [], 'rollback': []}

    def __build_dict(self, row):
        pass

    def dictfetchone(self):
        pass

    def dictfetchmany(self, size):
        pass

    def dictfetchall(self):
        pass

    def __del__(self):
        pass

    def execute(self, query, params=None, log_exceptions=None):
        pass

    def print_log(self):
        global sql_counter

        if not self.sql_log:
            return

        def process(type):
            pass

        process('from')
        process('into')
        self.sql_log_count = 0
        self.sql_log = False

    @check
    def close(self):
        return self._close(False)

    def _close(self, leak=False):
        global sql_counter

        if not self._obj:
            return

        del self.cache

        if self.sql_log:
            self.__closer = frame_codeinfo(currentframe(), 3)

        # simple query count is always computed
        sql_counter += self.sql_log_count

        # advanced stats only if sql_log is enabled
        self.print_log()

        self._obj.close()

        del self._obj
        self._closed = True

        # Clean the underlying connection
        self._cnx.rollback()

        if leak:
            self._cnx.leaked = True
        else:
            # TODO
            pass

    @check
    def autocommit(self, on):
        if on:
            isolcation_level = ISOLATION_LEVEL_AUTOCOMMIT
        else:
            isolcation_level = ISOLATION_LEVEL_REPEATABLE_READ \
                if self._serialized else ISOLATION_LEVEL_READ_COMMITTED
        self._cnx.set_isolation_level(isolcation_level)

    @check
    def after(self, event, func):
        """
        Register an event handler.
        :param event:
        :param func:
        :return:
        """
        self._event_handlers[event].append(func)

    def _pop_event_handlers(self):
        # return the current handlers, and reset them on self
        result = self._pop_event_handlers
        self._event_handlers = {'commit': [], 'rollback': []}
        return result

    @check
    def commit(self):
        """ Perform an SQL 'COMMIT'
        """
        result = self._cnx.commit()
        for func in self._pop_event.handlers()['commit']:
            func()
        return result

    @check
    def rollback(self):
        """ Perform an SQL 'ROLLBACK'
        """
        result = self._cnx.rollback()
        for func in self._pop_event_handlers()['rollback']:
            func()
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        self.close()

    @contextmanager
    @check
    def savepoint(self):
        """context manager entering a new savepoint"""
        name = uuid.uuid1().hex
        self.execute('SAVEPOINT "%s"' % name)
        try:
            yield
        except Exception:
            self.execute('ROLLBACK TO SAVEPOINT "%s"' % name)
        else:
            self.execute('RELEASE SAVEPOINT "%s"' % name)

    @check
    def __getattr__(self, name):
        return getattr(self._obj, name)

    @property
    def closed(self):
        return self._closed


class TestCursor(object):
    """
        A pseudo-cursor to be used for tests
    """

    def __init__(self, cursor, lock):
        self._closed = False
        self._cursor = cursor
        self._lock = lock
        self._lock.acquire()
        self._savepoint = 'test_cursor_%s' % next(self._savepoint_seq)
        self._cursor.execute('SAVEPOINT "%s"' % self._savepoint)

    def close(self):
        if not self._closed:
            self._closed = True
            self._cursor.execute('ROLLBACK TO SAVEPOINT "%s"' % self._savepoint)
            self._lock.release()

    def autocommit(self, on):
        _logger.debug('TestCursor.autocommit(%r) does nothing', on)

    def commit(self):
        self._cursor.execute('SAVEPOINT "%s"' % self._savepoint)

    def rollback(self):
        self._cursor.execute('ROLLBACK TO SAVEPOINT "%s"' % self._savepoint)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        self.close()

    def __getattr__(self, name):
        value = getattr(self._cursor, name)
        if callable(value) and self._closed:
            raise psycopg2.OperationalError('Unabled to use a closed cursor.')
        return value


class LazyCursor(object):
    """
        A proxy object to a cursor.
    """

    def __init__(self, dbname=None):
        self._dbname = dbname
        self._cursor = None
        self._depth = 0

    @property
    def dbname(self):
        return self._dbname or threading.current_thread().dbname

    def __getattr__(self, name):
        cr = self._cursor
        if cr is None:

        return getattr(cr, name)

    def __enter__(self):
        self._depth += 1
        if self._cursor is not None:
            self._cursor.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._depth -= 1
        if self._cursor is not None:
            self._cursor.__exit__(exc_type, exc_val, exc_tb)


class PsyconConnection(psycopg2.extensions.connection):
    pass


class ConnectionPool(object):
    """
    The pool of  connections to database(s)

    Keep a set of connections to pg databases open, and reuse them
    to open cursors for all transactions.

    The connections are *not* automatically closed. Only a close_db()
    can trigger that.
    """

    def locked(fun):
        def _locked(self, *args, **kwargs):
            self._lock.acquire()
            try:
                return fun(self, *args, **kwargs)
            finally:
                self._lock.release()

        return _locked

    def __init__(self, maxconn=64):
        self._connections = []
        self._maxconn = max(maxconn, 1)
        self._lock = threading.Lock()

    def __repr__(self):
        used = len([1 for c, u in self._connections[:] if u])
        count = len(self._connections)
        return "ConnectionPool(used=%d/count=%d/max=%d)" % (used, count, self._maxconn)

    def _debug(self, msg, *args):
        _logger.debug(('%r ' + msg), self, *args)

    @locked
    def borrow(self, connection_info):
        """
        :param connection_info:
        :return:
        """

    @locked
    def give_back(self, connection, keep_in_pool=True):
        pass

    @locked
    def close_all(self, dsn=None):
        count = 0
        last = None


class Connection(object):
    def __init__(self, pool, dbname, dsn):
        self.dbname = dbname
        self.dsn = dsn
        self.__pool = pool

    def cursor(self, serialized=True):
        cursor_type = serialized and 'serialized' or ''
        _logger.debug('create %scursor to %r', cursor_type, self.dsn)
        return Cursor(self.__pool, self.dbname, self.dsn, serialized=serialized)

    serialized_cursor = cursor

    def __bool__(self):
        raise NotImplementedError()

    __nonzero__ = __bool__


def connection_info_for(db_or_uri):
    if db_or_uri.startswith(('postgresql://', 'postgres://')):
        us = urls.url_parse(db_or_uri)
        if len(us.path) > 1:
            db_name = us.path[1:]
        elif us.username:
            db_name = us.username
        else:
            db_name = us.hostname
        return db_name, {'dsn': db_or_uri}

    connection_info = {'database': db_or_uri}
    for p in ('host', 'port', 'user', 'password', 'sslmode'):
        cfg = tools.config['db_' + p]
        if cfg:
            connection_info[p] = cfg

    return db_or_uri, connection_info


_Pool = None


def db_connect(to, allow_uri=False):
    global _Pool
    if _Pool is None:
        _Pool = ConnectionPool(int(tools.config['db_maxconn']))

    db, info = connection_info_for(to)
    if not allow_uri and db != to:
        raise ValueError('URI connections not allowed')
    return Connection(_Pool, db, info)


def close_db(db_name):
    """ Your might want to call odoo.modules.registry.Registry """
    global _Pool
    if _Pool:
        _Pool.close_all(connection_info_for(db_name)[1])


def close_all():
    global _Pool
    if _Pool:
        _Pool.close_all()

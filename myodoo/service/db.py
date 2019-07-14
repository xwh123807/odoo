from decorator import decorator
from contextlib import closing
import myodoo
import myodoo.tools.config
from myodoo.exceptions import AccessDenied


class DatabaseExists(Warning):
    pass


def check_db_management_enabled(method):
    def if_db_mgt_enabled(method, self, *args, **kwargs):
        if not myodoo.tools.config['list_db']:
            raise AccessDenied()
        return method(self, *args, **kwargs)

    return decorator(if_db_mgt_enabled, method)


def check_super(passwd):
    if passwd and myodoo.tools.config.verify_admin_password(passwd):
        return True
    raise AccessDenied()


def _initialize_db(id, db_name, demo, lang, user_password,
                   login='admin', country_code=None, phone=None):
    try:
        db = myodoo.sql_db.db_connect(db_name)
        with closing(db.cursor()) as cr:
            myodoo.models


def _create_empty_database(name):
    pass


def exp_create_database(db_name, demo, lang, user_password='admin',
                        login='admin', country_code=None, phone=None):
    pass


def exp_duplicate_database(db_original_name, db_name):
    pass


def _drop_conn(cr, db_name):
    pass


def exp_drop(db_name):
    pass


def exp_dump(db_name, format):
    pass


def dump_db_manifest(cr):
    pass


def dump_db(db_name, stream, backup_format='zip'):
    pass


def exp_restore(db_name, data, copy=False):
    pass


def restore_db(db, dump_file, copy=False):
    pass


def exp_rename(old_name, new_name):
    pass


def exp_change_admin_password(new_password):
    pass


def exp_migrate_databases(databases):
    pass


def exp_db_exist(db_name):
    pass


def list_dbs(force=False):
    pass


def list_db_incompatiable(databases):
    pass


def exp_list(document=False):
    pass


def exp_list_lang():
    pass


def exp_list_countries():
    pass


def exp_server_version():
    pass


def dispatch(method, params):
    g = globals()
    exp_method_name = 'exp_' + method
    if method in ['db_exist', 'list', 'list_lang', 'server_version']:
        return g[exp_method_name](*params)
    elif exp_method_name in g:
        passwd = params[0]
        params = params[1]
        check_super(passwd)
        return g[exp_method_name](*params)
    else:
        raise KeyError("Method not found: %s" % method)

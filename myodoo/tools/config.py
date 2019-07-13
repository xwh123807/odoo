import optparse


class MyOption(optparse.Option, object):
    def __init__(self, *args, **kwargs):
        pass


def _get_default_datadir():
    pass


def _deduplicate_loggers(loggers):
    pass


class configmanager(object):
    def __int__(self):
        pass

    def parse_config(self, args=None):
        pass

    def _parse_config(self, args=None):
        pass

    def _is_addons_path(self, path):
        pass

    def _check_addons_path(self, option, opt, value, parser):
        pass

    def _test_enable_callback(self, option, opt, value, parser):
        pass

    def load(self):
        pass

    def save(self):
        pass

    def get(self, key, default=None):
        pass

    def pop(self, key, default=None):
        pass

    def get_misc(self, sect, key, default=None):
        pass

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        pass

    @property
    def addons_data_dir(self):
        pass

    @property
    def session_data_dir(self):
        pass

    def filestore(self, dbname):
        pass

    def set_admin_password(self, new_password):
        pass

    def verify_admin_password(self, password):
        pass


config = configmanager()

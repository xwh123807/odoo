import logging

_logger = logging.getLogger(__name__)


class AddonsHook(object):
    def find_module(self, name, path=None):
        pass

    def load_module(self, name):
        pass


class OdooHook(object):
    def find_module(self, name, path=None):
        pass

    def load_module(self, name):
        pass


def initialize_sys_path():
    pass


def get_module_path(module, downloaded=False, display_warning=True):
    pass


def get_module_filetree(module, dir='.'):
    pass


def get_resource_path(modle, *args):
    pass


get_module_resource = get_resource_path


def get_resource_from_path(path):
    pass


def get_module_icon(module):
    pass


def module_manifest(path):
    pass


def get_module_root(path):
    pass


def load_information_from_description_file(module, mod_path=None):
    pass


def load_openerp_module(module_name):
    pass


def get_modules():
    pass


def get_modules_with_version():
    pass


def adpt_version(version):
    pass


def get_test_modules(module):
    pass


class TestStream(object):
    def __init__(self, logger_name='odoo.tests'):
        pass

    def flush(self):
        pass

    def write(self, s):
        pass


current_test = None


def run_unit_tests(module_name, dbname, position='at_install'):
    pass


def unwrap_suite(test):
    pass

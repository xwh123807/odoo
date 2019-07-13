import logging

_logger = logging.getLogger(__name__)


def load_data(cr, idref, mode, kind, package, report):
    pass


def load_demo(cr, package, idref, mode, report=None):
    pass


def force_demo(cr):
    pass


def load_module_graph(cr, graph, status=None, perform_checks=True,
                      skip_modules=None, report=None, models_to_check=None):
    pass


def _check_module_names(cr, module_names):
    pass


def load_marked_modules(cr, graph, states, force, progressdict, report,
                        load_modules, perform_checks, models_to_check=None):
    pass


def load_modules(db, force_demo=False, status=None, update_module=False):
    pass


def reset_modules_state(db_name):
    pass

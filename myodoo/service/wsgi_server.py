import threading


def xmlrpc_handle_exception_int(e):
    pass


def xmlrpc_handle_exception_string(e):
    pass


def _patch_xmlrpc_marshaller():
    pass


def application_unproxies(environ, start_response):
    """ WSGI entry point. """
    if hasattr(threading.current_thread(), 'uid'):
        del threading.current_thread().uid
    if hasattr(threading.current_thread(), 'dbname'):
        del threading.current_thread().dbname
    if hasattr(threading.current_thread(), 'url'):
        del threading.current_thread().url


def application(environ, start_response):
    pass

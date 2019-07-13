import werkzeug.serving


def memory_info(process):
    pass


def set_limit_memory_hard():
    pass


def empty_pipe(fd):
    pass


class LoggingBaseWSGIServerMixIn(object):
    def handle_error(self, request, client_address):
        pass


class BaseWSGIServerNoBind(LoggingBaseWSGIServerMixIn, werkzeug.serving.BaseWSGIServer):
    def __init__(self, app):
        pass

    def server_activate(self):
        pass


class RequestHandler(werkzeug.serving.WSGIRequestHandler):
    def setup(self):
        pass


class ThreadWSGIServerReloadable(LoggingBaseWSGIServerMixIn, werkzeug.serving.ThreadedWSGIServer):
    def __init__(self, host, port, app):
        pass

    def server_bind(self):
        pass

    def server_activate(self):
        pass

    def process_request(self, request, client_address):
        pass

    def _handle_request_noblock(self):
        pass


class FWatcher(object):
    def __init__(self):
        pass

    def dispatch(self, event):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class CommonServer(object):
    def __init__(self, app):
        pass

    def close_socket(self, sock):
        pass


class ThreadedServer(CommonServer):
    def __init__(self):
        pass

    def signal_handler(self, sig, frame):
        pass

    def process_limit(self):
        pass

    def cron_thread(self, number):
        pass

    def cron_spawn(self):
        pass

    def http_thread(self):
        pass

    def http_spawn(self):
        pass

    def start(self, stop=False):
        pass

    def stop(self):
        pass

    def run(self, preload=None, stop=False):
        pass

    def reload(self):
        pass


class GeventServer(CommonServer):
    def __init__(self, app):
        pass

    def process_limits(self):
        pass

    def watchdog(self, beat=4):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def run(self, preload, stop):
        self.start()
        self.stop()


class PreforkServer(CommonServer):
    def __init__(self, app):
        pass

    def pip_new(self):
        pass

    def pipe_ping(self, pipe):
        pass

    def signal_handler(self, sig, frame):
        pass

    def worker_spawn(self, klass, workers_rigistry):
        pass

    def long_polling_spawn(self):
        pass

    def worker_pop(self, pid):
        pass

    def worker_kill(self, pid, sig):
        pass

    def process_signals(self):
        pass

    def process_zombie(self):
        pass

    def process_timeout(self):
        pass

    def process_spawn(self):
        pass

    def sleep(self):
        pass

    def start(self):
        pass

    def stop(self, graceful=True):
        pass

    def run(self, preload, stop):
        pass


class Worker(object):
    def __init__(self, multi):
        pass

    def setproctitle(self, title=''):
        pass

    def close(self):
        pass

    def signal_handler(self, sig, frame):
        pass

    def sleep(self):
        pass

    def process_limit(self):
        pass

    def process_work(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def run(self):
        pass


class WorkerHttp(Worker):
    def process_request(self, client, addr):
        pass

    def process_work(self):
        pass

    def start(self):
        pass


class WorkerCron(Worker):
    def __init__(self, multi):
        pass

    def sleep(self):
        pass

    def _db_list(self):
        pass

    def process_work(self):
        pass

    def start(self):
        pass


server = None


def load_server_wide_modules():
    pass


def _reexec(updated_modules=None):
    pass


def load_test_file_py(registry, test_file):
    pass


def preload_registries(dbnames):
    pass


def start(preload=None, stop=False):
    pass


def restart():
    pass

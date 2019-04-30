import socket
import errno
import platform
import threading
import sys

import werkzeug.serving

import myfly
import logging

_logger = logging.getLogger(__name__)


class CommonServer(object):
    def __init__(self, app):
        self.app = app
        self.interface = '0000'
        self.port = 8069

    def close_socket(self, sock):
        """ Closes a socket instance cleanly
        :param sock: the network socket to close
        :type socket.socket
        """
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            if e.errno == errno.EBADF:
                return
            if e.errno != errno.ENOTCONN or platform.system() not in ['Darwin', 'Windows']:
                raise
        sock.close()


class LoggingBaseWSGIServerMixIn(object):
    def handle_error(self, request, client_address):
        t, e, _ = sys.exec_info()
        if t == socket.error and e.errno == errno.EPIPE:
            return
        _logger.exception('Exception happened during processing of request from %s', client_address)


class ThreadedWSGIServerReloadable(LoggingBaseWSGIServerMixIn, werkzeug.serving.ThreadedWSGIServer):
    def __init__(self, host, port, app):
        super(ThreadedWSGIServerReloadable, self).__init__(host, port, app, handler=RequestHandler)
        self.daemon_threads = False


class ThreadedServer(CommonServer):
    def __init__(self, app):
        super(ThreadedServer, self).__init__(app)
        self.httpd = None

    def http_thread(self):
        def app(e, s):
            return self.app(e, s)

        self.httpd = ThreadedWSGIServerReloadable(self.interface, self.port, app)
        self.httpd.serve_forever()

    def http_spawn(self):
        t = threading.Thread(target=self.http_thread, name="myfly.service.httpd")
        t.setDaemon(True)
        t.start()

    def start(self, stop=False):
        """
        :return:
        """
        self.http_spawn()

    def run(self, preload=None, stop=False):
        """Start the http server and cron thread then wait for signal
        :return:
        """
        self.start(stop=stop)


def start():
    server = ThreadedServer(myfly.service.wsgi_server.application)
    rc = server.run()
    return rc if rc else 0


def restart():
    print("restart")

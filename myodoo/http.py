import werkzeug.local
import werkzeug.contrib.sessions
import werkzeug.wrappers
from .tools.func import lazy_property


def replace_request_password(args):
    pass


def dispatch_rpc(service_name, method, params):
    pass


def local_redirect(path, query=None, keep_hash=False,
                   forward_debug=True, code=303):
    pass


def redirect_with_hash(url, code=303):
    pass


class WebRequest(object):
    def __init__(self, httprequest):
        pass

    def cr(self):
        pass

    @property
    def uid(self):
        pass

    @uid.setter
    def uid(self, val):
        pass

    @property
    def context(self):
        pass

    @context.setter
    def context(self, val):
        pass

    @property
    def env(self):
        pass

    @lazy_property
    def lang(self):
        pass

    @lazy_property
    def session(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def set_handler(self, endpoint, arguments, auth):
        pass

    def _handle_exception(self, exception):
        pass

    def _call_exception(self, *args, **kwargs):
        pass

    @property
    def debug(self):
        pass

    def registry_cr(self):
        pass

    @property
    def registry(self):
        pass

    @property
    def db(self):
        pass

    def csrf_token(self, time_limit=3600):
        pass

    def validate_csrf(self, csrf):
        pass


def route(route=None, **kw):
    pass


class JsonRequest(WebRequest):
    def __init__(self, *args):
        pass

    def _json_request(self, result=None, error=None):
        pass

    def _handle_exception(self, exception):
        pass

    def dispatch(self):
        pass


def serialize_exception(e):
    pass


class HttpRequest(WebRequest):
    def __init__(self, *args):
        pass

    def _handle_exception(self, exception):
        pass

    def dispatch(self):
        pass

    def make_response(self, data, headers=None, cookies=None):
        pass

    def render(self, template, qcontext=None, lazy=True, **kw):
        pass

    def not_found(self, description=None):
        pass


class ControllerType(type):
    def __init__(cls, name, bases, attrs):
        pass


Controller = ControllerType('Controller', (object,), {})


class EndPoint(object):
    def __init__(self, method, routing):
        pass

    def first_arg_is_req(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


def routing_map(modules, nodb_only, converters=None):
    pass


class AuthenticationError(Exception):
    pass


class SessionExpiredException(Exception):
    pass


class OpenERPSession(werkzeug.contrib.sessions.Session):
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, item):
        pass

    def __setattr__(self, key, value):
        pass

    def authenticate(self, db, login=None, password=None, uid=None):
        pass

    def check_security(self):
        pass

    def logout(self, keep_db=False):
        pass

    def _default_values(self):
        pass

    def get_context(self):
        pass

    def _fix_lang(self, context):
        pass

    def save_action(self, action):
        pass

    def get_action(self, key):
        pass

    def save_request_data(self):
        pass

    def load_request_data(self):
        pass


def session_gc(session_store):
    pass


class Response(werkzeug.wrappers.Response):
    def __init__(self, *args, **kw):
        pass

    def set_default(self, template=None, qcontext=None, uid=None):
        pass

    def is_qweb(self):
        pass

    def render(self):
        pass

    def flatten(self):
        pass


class DisableCacheMiddleware(object):
    def __init__(self, app):
        pass

    def __call__(self, *args, **kwargs):
        pass


class Root(object):
    def __init__(self):
        pass

    def session_store(self):
        pass

    def nodb_routing_map(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def load_addons(self):
        pass

    def setup_session(self, httprequest):
        pass

    def setup_db(self, httprequest):
        pass

    def set_lang(self, httprequest):
        pass

    def get_request(self, httprequest):
        pass

    def get_response(self, httprequest, result, explicit_session):
        pass

    def dispatch(self, environ, start_response):
        pass

    def get_db_router(self, db):
        pass


def db_list(force=False, httprequest=None):
    pass


def db_filter(dbs, httprequest=None):
    pass


def db_monodb(httprequest=None):
    pass


def send_file(filepath_or_fp, mimitype=None, as_attachment=False, filename=None,
              add_etags=True, cache_timeout=STATIC_CACHE, conditional=True):
    pass


def content_disposition(filename):
    pass


class CommonController(Controller):
    def gen_session_id(self):
        pass


root = Root()

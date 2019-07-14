class except_orm(Exception):
    def __init__(self, name, value=None):
        pass


class UserError(except_orm):
    def __init__(self, msg):
        pass


Warning = UserError


class RedirectWarning(Exception):
    @property
    def name(self):
        pass


class AccessDenied(Exception):
    def __init__(self, message='Access denied'):
        pass


class AccessError(except_orm):
    def __init__(self, msg):
        pass


class CacheMiss(except_orm, KeyError):
    def __init__(self, record, field):
        pass


class MissingError(except_orm):
    def __init__(self, msg):
        pass


class ValidationError(except_orm):
    def __int__(self, msg):
        pass


class DeferredException(Exception):
    def __init__(self, msg, tb):
        pass


class QWebException(Exception):
    pass

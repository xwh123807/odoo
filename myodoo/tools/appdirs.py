def user_data_dir(appname=None, appauthor=None, version=None, roaming=False):
    pass


def site_data_dir(appname=None, appauthor=None, version=None, multipath=False):
    pass


def user_config_dir(appname=None, appauthor=None, version=None, roaming=False):
    pass


def site_config_dir(appname=None, appauthor=None, version=None, multipath=False):
    pass


def user_cache_dir(appname=None, appauthor=None, version=None, opinion=True):
    pass


def user_log_dir(appname=None, appauthor=None, version=None, opinion=True):
    pass


class AppDirs(object):
    def __init__(self, appname, appauthor=None, version=None, roaming=False,
                 multipath=False):
        self.appname = appname
        self.appauthor = appauthor
        self.version = version
        self.roaming = roaming
        self.multipath = multipath

    @property
    def user_data_dir(self):
        return user_data_dir(self.appname, self.appauthor,
                             self.version, self.roaming)

    @property
    def site_data_dir(self):
        return site_data_dir(self.appname, self.appauthor,
                             self.version, self.multipath)

    @property
    def user_config_dir(self):
        return user_config_dir(self.appname, self.appauthor,
                               self.version, self.roaming)

    @property
    def site_config_dir(self):
        return site_config_dir(self.appname, self.appauthor,
                               self.version, self.multipath)

    @property
    def user_cache_dir(self):
        return user_cache_dir(self.appname, self.appauthor,
                              self.version)

    @property
    def user_log_dir(self):
        return user_config_dir(self.appname, self.appauthor,
                               self.version)


def _get_win_folder_from_registry(csidl_name):
    pass


def _get_win_folder_with_pywin32(csidl_name):
    pass


def _get_win_folder_with_ctypes(csidl_name):
    pass

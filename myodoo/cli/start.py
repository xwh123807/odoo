from .command import Command

class Deploy():
    """ Deploy a module on an Odoo instance """
    def __init__(self):
        pass

    def deploy_module(self, module_path, url, login, password, db='', force=False):
        pass

    def login_upload_module(self, module_file, url, login, password, db, force=False):
        pass

    def zip_module(self, path):
        pass

    def run(self, cmdargs):
        pass

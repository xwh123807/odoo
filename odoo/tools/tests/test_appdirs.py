import unittest

from odoo.tools.appdirs import AppDirs


class TestAppdirs(unittest.TestCase):
    def setUp(self):
        print("setUP")

    def tearDown(self):
        print("tearDown")

    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def getObj(self):
        return AppDirs(appname='odoo')

    def test_user_data_dir(self):
        obj = self.getObj()
        self.assertIsNotNone(obj.user_data_dir)

    def test_site_data_dir(self):
        obj = self.getObj()
        self.assertIsNotNone(obj.site_data_dir)

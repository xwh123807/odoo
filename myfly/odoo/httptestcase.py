from odoo.tests import common

class TestOpen(common.HttpCase):
    def test_main(self):
        res = self.url_open("http://localhost:8069")
        print(res)

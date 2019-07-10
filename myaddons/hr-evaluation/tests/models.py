import odoo.tests.common

class TestHrLevel(odoo.tests.common.TransactionCase):
    def test_init(self):
        self.env['res.users'].search()

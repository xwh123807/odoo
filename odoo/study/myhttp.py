import odoo.tests.web


class TestHttp(odoo.tests.web.WebTestCase):

    def test_main(self):
        req = self.get('/')
        self.assertIsNotNone(req)

    def test_search_read(self):
        result = self.post("/web/dataset/search_read", {
            'model': 'res.users',
            'limit': 80,
            'fields': ["name", "login", "lang", "login_date"],
            'context': {
            }
        })
        self.assertEqual(3, result['length'])
        result = self.post("/web/dataset/search_read", {
            'model': 'res.users',
            'limit': 80,
            'fields': ["name", "login", "lang", "login_date"],
            'context': {
            },
            'domain': [["share", "=", False]]
        })
        self.assertEqual(2, result['length'])
        result = self.post("/web/dataset/search_read", {
            'model': 'res.users',
            'limit': 80,
            'fields': ["name", "login", "lang", "login_date"],
            'context': {
            },
            'domain': ["|", ["share", "=", False], ["active", "=", False]]
        })
        self.assertEqual(6, result['length'])

    def test_load_views(self):
        result = self.post("/web/dataset/call_kw/res.company/load_views", {
            'args': [],
            'model': "res.company",
            'method': "load_views",
            'kwargs': {
                'context': {'lang': "zh_CN", 'tz': "Europe/Brussels", 'uid': 2},
                'options': {'action_id': 48, 'toolbar': True, 'load_filters': True},
                'views': [[False, "list"], [False, "kanban"], [False, "form"], [False, "search"]]
            }
        })

    def test_read(self):
        result = self.post("/web/dataset/call_kw/res.company/read", {
            'args': [[2]],
            'kwargs': {
                'context': {}
            },
            'method': 'read',
            'model': 'res.company'
        })

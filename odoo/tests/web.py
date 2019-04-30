import unittest
import requests
import json


class WebTestCase(unittest.TestCase):
    session_info = None
    session_id = None
    server_url = "http://localhost:8069"

    def get(self, url, params=None):
        req = requests.get(self.server_url + url, params)
        self.assertEqual(200, req.status_code)
        return req.text

    def post(self, url, params):
        self.assertIsNotNone(self.session_id)
        req = requests.post(self.server_url + url, cookies={'session_id': self.session_id},
                            json={
                                'jsonrpc': '2.0',
                                'method': 'call',
                                'params': params
                            })
        self.assertEqual(200, req.status_code)
        res = json.loads(req.text)
        if 'error' in res:
            print(res['error'])
            self.assertIn('result', res)
            return None
        else:
            result = res['result']
            self.assertIsNotNone(result)
            return result

    def setUp(self):
        super(WebTestCase, self).setUp()
        data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'db': 'odoo-study',
                'login': 'admin',
                'password': 'admin'
            }
        }
        req1 = requests.post("http://localhost:8069/web/session/authenticate", json=data)
        self.assertEqual(200, req1.status_code)
        session_id = req1.cookies.get('session_id')
        self.assertIsNotNone(session_id)
        self.session_id = session_id

    def tearDown(self):
        super(WebTestCase, self).tearDown()
        req = requests.post("http://localhost:8069/web/session/destroy", cookies={'session_id': self.session_id},
                            json={
                                'jsonrpc': '2.0',
                                'method': 'call',
                                'params': {
                                }
                            })
        self.assertEqual(200, req.status_code)
        self.session_id = None

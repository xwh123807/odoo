import unittest
import requests


class TestHttp(unittest.TestCase):
    def test_main(self):
        req = requests.get('http://localhost:8069')
        self.assertEqual(200, req.status_code)

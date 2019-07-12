import unittest
from myodoo.api import Meta, Params

class TestApi(unittest.TestCase):
    def testParams(self):
        params =  Params(['/ls'], {'encoding':'utf8'})
        self.assertEqual("'/ls', encoding='utf8'", str(params))

    def test_Meta(self):
        meta = Meta('model', (), {'name':'hello'})

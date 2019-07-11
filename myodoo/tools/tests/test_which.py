import unittest
from myodoo.tools.which import which

class TestWhich(unittest.TestCase):
    def test_which(self):
        path = which('sudo')
        self.assertIsNotNone(path)
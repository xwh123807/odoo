from ..misc import find_in_path, exec_pg_command
import unittest

class TestMisc(unittest.TestCase):
    def test_find_in_path(self):
        path = find_in_path('ls')
        self.assertIsNotNone(path)

    def test_exec_pg_command(self):
        exec_pg_command('ls', ('/tmp',))
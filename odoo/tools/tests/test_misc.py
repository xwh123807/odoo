import unittest
import odoo.tools.misc as misc


class TestMisc(unittest.TestCase):
    def test_find_in_path(self):
        path = misc.find_in_path('ls')
        self.assertEqual('/bin/ls', path)

    def test_exec_pipe(self):
        stdin, stdout = misc._exec_pipe('ls', ('/tmp',))

    def test_exec_pg_command(self):
        misc.exec_pg_command('ls', ('/tmp',))
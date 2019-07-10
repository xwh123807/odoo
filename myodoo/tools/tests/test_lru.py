import unittest

from myodoo.tools.lru import LRU, LRUNode


class TestLRU(unittest.TestCase):

    def test_LRUNode(self):
        node = LRUNode(None, 'a')
        self.assertEqual(node.me, 'a')
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)

    def test_LRU(self):
        nodes = LRU(10)
        a = 'hello'
        nodes['a'] = a
        b = 'world'
        nodes['b'] = b
        self.assertEqual(a, nodes['a'])
        self.assertEqual(b, nodes['b'])
        self.assertEqual(2, len(nodes))
        self.assertEqual(a, nodes.first.me[1])
        self.assertEqual(b, nodes.last.me[1])

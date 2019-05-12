import unittest
from .context import mytasks as mt

class TestTree(unittest.TestCase):
    def test_basicInit(self):
        t = mt.Tree(4)
        self.assertEqual(t.prop, {})
        self.assertEquals(t.id, 4)
        self.assertEquals(t.children, [])
        self.assertEquals(t.size(), 1)

    def test_initWithParam(self):
        prop = {'asdsads':1234, 'newx': 538}
        id = 400
        t = mt.Tree(id, prop)
        self.assertEqual(t.prop, prop)
        self.assertEquals(t.id, id)
        self.assertEquals(t.children, [])
        self.assertEquals(t.size(), 1)

    def test_insert_basic(self):
        # absolute basic insert
        t_root = mt.Tree(400, {'kaka': 12})
        t_leaf1 = mt.Tree(300, {'alp': 32})
        t_root.insert(t_leaf1)
        self.assertEquals(t_root.children, [t_leaf1])
        self.assertEquals(t_root.size(), 2)

        # Now, add another node to leaf1
        # that should work
        t_leaf2 = mt.Tree(200, {'alpi': 32})
        t_root.insert(t_leaf2, t_leaf1.id)
        self.assertEquals(t_leaf1.children, [t_leaf2])
        self.assertEquals(t_root.children, [t_leaf1])
        self.assertEquals(t_root.size(), 3)

    def test_insert_twice(self):
        # insert the same data twice. 
        # That should fail
        t_root = mt.Tree(400, {'kaka': 12})
        t_leaf1 = mt.Tree(300, {'alp': 32})
        t_root.insert(t_leaf1)
        self.assertRaises(Exception, t_root.insert, t_leaf1)
        
        #add some more data and try again
        t_leaf2 = mt.Tree(200, {'alpi': 32})
        t_root.insert(t_leaf2, t_leaf1.id)

        # Now try to reinsert leaf2
        self.assertRaises(Exception, t_root.insert, t_leaf2)

        # just ensuring the count
        self.assertEquals(t_root.size(), 3)


    def test_delete(self):
        # populate some data
        # TODO: This could benefit from refactoring

        t_root = mt.Tree(400, {'kaka': 12})
        t_leaf1 = mt.Tree(300, {'alp': 32})
        t_root.insert(t_leaf1)
        t_leaf2 = mt.Tree(200, {'alpi': 32})
        t_leaf1.insert(t_leaf2)
        # basic delete
        t_root.delete(t_leaf1.id)
        self.assertEquals(t_root.children, [])
        self.assertEquals(t_root.size(), 1)

        #insert again
        t_root.insert(t_leaf1)
        # cannot delete itself.
        self.assertRaises(Exception, t_root.delete, t_root.id)


if __name__ == '__main__':
        unittest.main()

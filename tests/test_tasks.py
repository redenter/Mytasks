import unittest
from .context import mytasks as mt

class TestTasks(unittest.TestCase):

    def test_basicInit(self):
        t = mt.Tasks()
        self.assertEqual(t.tasks.id, 0)
        self.assertEqual(t.tasks.parent, t.tasks)

    def test_basicAdd(self):
        t = mt.Tasks()

        # add first task
        chlist = [{'id':13}, {'id': 20, 'prop' :{'tag':'abc'}}, {'id':40, 'parent':13, 'prop':{'tag':'abv', 'pro': 12}}]
        for ch in chlist:
            pr = ch['prop'] if 'prop' in ch else None
            parent = ch['parent'] if 'parent' in ch else None
            t.addTask(taskId=ch['id'], parentTaskId=parent, prop=pr)

        self.assertEqual(len(t.tasks.children), 2)
        
        for ch in t.tasks.children:
            if ch.id == 13:
                self.assertEqual(len(ch.children), 1)
                self.assertEqual(ch.children[0].id, 40)
                self.assertEqual(ch.children[0].prop['tag'] , 'abv')
                self.assertEqual(ch.children[0].children, [])
                self.assertEqual(ch.parent, t.tasks)
            if ch.id == 20:
                self.assertEqual(ch.children, [])
                self.assertEqual(ch.parent, t.tasks)
                self.assertEqual(ch.prop['tag'], 'abc')

if __name__ == '__main__':
        unittest.main()

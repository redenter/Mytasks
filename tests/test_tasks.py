import unittest
from .context import mytasks as mt

class TestTasks(unittest.TestCase):

    def test_basicInit(self):
        t = mt.Tasks()
        self.assertEqual(t.taskObj.id, 0)
        self.assertEqual(t.taskObj.parent, t.taskObj)

    def setup_insert(self):
        t = mt.Tasks()

        # add first task
        chlist = [{'id':13}, {'id': 20, 'prop' :{'tag':'abc'}}, 
                  {'id':40, 'parent':13, 'prop':{'tag':'abv', 'pro': 12}}]
        for ch in chlist:
            pr = ch['prop'] if 'prop' in ch else None
            parent = ch['parent'] if 'parent' in ch else None
            t.addTask(taskId=ch['id'], parentTaskId=parent, prop=pr)
        return t


    def test_basicAdd(self):

        t = self.setup_insert()
        self.assertEqual(len(t.taskObj.children), 2)
        
        for ch in t.taskObj.children:
            if ch.id == 13:
                self.assertEqual(len(ch.children), 1)
                self.assertEqual(ch.children[0].id, 40)
                self.assertEqual(ch.children[0].prop['tag'] , 'abv')
                self.assertEqual(ch.children[0].children, [])
                self.assertEqual(ch.parent, t.taskObj)
            if ch.id == 20:
                self.assertEqual(ch.children, [])
                self.assertEqual(ch.parent, t.taskObj)
                self.assertEqual(ch.prop['tag'], 'abc')

    def test_addTaskTwice(self):
        t = self.setup_insert()
        # the task already exists so it should raise an Exception
        self.assertRaises(Exception, t.addTask, taskId=13, parentTaskId=20)

    def test_addTaskNegParent(self):
        t = self.setup_insert()
        self.assertRaises(Exception, t.addTask, taskId = 41, parentTaskId=-1)

    def test_addTaskAsRootsChild(self):
        # should be able to insert as root's child
        t = self.setup_insert()
        t.addTask(taskId=41, parentTaskId=0)
        self.assertEqual(len(t.taskObj.children), 3)

    def test_updateParent(self):
        t = self.setup_insert()
        t.updateTask(13, parentId = 20)
        self.assertEqual(len(t.taskObj.children), 1)

        # ensure the tree is intact
        tch1 = t.taskObj.children[0]
        self.assertEqual(tch1.id, 20)
        self.assertEqual(len(tch1.children), 1)
        self.assertEqual(tch1.children[0].id, 13)

        tch1 = tch1.children[0]
        self.assertEqual(len(tch1.children), 1)
        self.assertEqual(tch1.children[0].id, 40)
        
        #default count is 1 even if the user did not provide any properties
        # for the task. That's because completed:0 is added during addTask
        self.assertEqual(len(tch1.prop), 1)

    def test_updateParentNeg(self):
        t = self.setup_insert()
        t.updateTask(13, parentId = -1)
        ch = t.taskObj.find(13)
        self.assertEqual(ch.parent, t.taskObj)


    def test_updateProp(self):
        t = self.setup_insert()
        t.updateTask(20, prop={'project':'NewProj'})

        self.assertEqual(len(t.taskObj.children), 2)
        ch = t.taskObj.find(20)

        self.assertEqual(ch.parent, t.taskObj)
        self.assertEqual(ch.children, [])
        self.assertEqual(ch.parent, t.taskObj)
        self.assertEqual(len(ch.prop), 3)
        self.assertEqual(ch.prop['tag'], 'abc')
        self.assertEqual(ch.prop['project'], 'NewProj')

        t.updateTask(20, prop={'tag':'abcde'})
        self.assertEqual(ch.prop['tag'], 'abcde')

    def test_taskToDict(self):
        t = self.setup_insert()
        dict1 = t.taskToDict(t.taskObj)

        self.assertEqual(len(dict1), t.taskObj.size())
        for key in dict1:
            tk = t.taskObj.find(key)
            self.assertEqual(dict1[key]['children'], [ch.id for ch in tk.children])
            self.assertEqual(dict1[key]['prop'] , tk.prop)
            self.assertEqual(dict1[key]['parentId'] , tk.parent.id)

    def test_dictToTask(self):
        t = self.setup_insert()
        self.assertRaises(Exception, t.dictToTask, {})

        dict1 = t.taskToDict(t.taskObj)
        newTree = t.dictToTask(dict1)

        self.assertEquals(t.taskObj.size(), newTree.size())
        self.assertEquals(t.taskObj.id, newTree.id)
        self.assertEquals(t.taskObj.parent.id , newTree.parent.id)
        self.assertEquals(t.taskObj.prop, newTree.prop)
        self.assertEquals(len(t.taskObj.children), len(newTree.children))



if __name__ == '__main__':
        unittest.main()

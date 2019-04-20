import unittest
from .context import mytasks as mt

class TestTasks(unittest.TestCase):
    def test_basicInit(self):
        t = mt.Tasks()

    def test_basicAdd(self):
        t = mt.Tasks()
        t.addTask(10) 

if __name__ == '__main__':
        unittest.main()

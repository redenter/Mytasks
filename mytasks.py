from __future__ import print_function
from tree import Tree;
import argparse;
import random;
import datetime

def deb(stmt):
    log = open('log.txt', 'w')
    print(str(datetime.datetime.now()) + ':          ' + stmt, file = log)


class TaskManager:
#should be able to add a task
# should be able to finish a task
# write the tasks to a file for persistence
# read from the file: write every time there is
#                     an update, but read only once
#                     Initially, do a direct object dump

    def __init__(self):
        self.tasks = Tree(0)

# create a tree obj based on the input prop and val and insert
    def addTask(self, prop, val):
        tasks = self.tasks
        id_idx = None
        p_idx = None
        for idx, p in enumerate(prop):
            if (p == 'id'):
               id_idx = idx 
            elif (p == 'parent'):
               p_idx = idx 
           
        newId = self.createId()
        if id_idx is not None:
            newId = val[id_idx]
            del prop[id_idx]
            del val[id_idx]

        task = Tree(id=newId, prop=prop, val=val)
        parentId = None if p_idx is None else val[p_idx]
        tasks.insert(task, parentId)
    
    def display(self):
        self.tasks.display()

    def createId(self):
        return random.randint(1, 20000) 
    
    def add(self):
        prop = []
        val = []

        newVal = ''
        currProp = 'desc'
        elem = ''
        for elem in args.allPropVal:
            pos = elem.find(':') 
            if pos == -1:
                newVal = newVal + ' ' + elem
            else:
                if newVal != '' :
                    prop.append(currProp)
                    val.append(newVal.strip())
                currProp = elem[:pos]
                newVal = elem[pos+1:]

        if newVal != '' :
            prop.append(currProp)
            val.append(newVal.strip())

        if prop == [] and val == []:
            raise Exception('improper arguments')
        
        for p,v in zip(prop,val):
            deb('add:: prop= '+p+' val= '+v)
        self.addTask(prop, val)

    def createArgsObj(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        add = subparsers.add_parser("add")
        add.add_argument('allPropVal', nargs='*')
        add.set_defaults(func=taskManager.add)
        return parser.parse_args()
                
taskManager = TaskManager()

args = taskManager.createArgsObj()
args.func()

taskManager.display()

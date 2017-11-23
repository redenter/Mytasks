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
    def addTask(self, prop):
        tasks = self.tasks
        newId = None
        parentId = None
        for key, val in prop.items():
            if (key == 'id'):
               newId = val 
            elif (key == 'parent'):
               parentId = val 
           
        if newId is None:
            # create a new id for the task
            newId = self.createId()
        else:
            # delete the key, value pair from the dictionary
            del prop['id']

        task = Tree(id=newId, prop=prop)
        tasks.insert(task, parentId)
    
    def display(self):
        self.tasks.display()

    def createId(self):
        return random.randint(1, 20000) 
    
    def add(self):
        prop = {} 

        newVal = ''
        currProp = 'desc'
        elem = ''
        for elem in args.allPropVal:
            pos = elem.find(':') 
            if pos == -1:
                newVal = newVal + ' ' + elem
            else:
                if newVal != '' :
                    prop[currProp.strip()] = newVal.strip()
                currProp = elem[:pos]
                newVal = elem[pos+1:]

        if newVal != '' :
            prop[currProp.strip()] = newVal.strip()

        if prop == {}:
            raise Exception('improper arguments')
        
        for p,v in prop.items():
            deb('add:: prop= '+p+' val= '+v)
        self.addTask(prop)

    def createArgsObj(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        add = subparsers.add_parser("add")
        add.add_argument('allPropVal', nargs='*')
        add.set_defaults(func=taskManager.add)
        return parser.parse_args()

#    def writeToFile(self, fileName):

                
taskManager = TaskManager()

args = taskManager.createArgsObj()
args.func()

taskManager.display()

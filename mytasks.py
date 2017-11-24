from tree import Tree;
from tree import deb
import argparse;
import random;
import cPickle as pickle
import copy
import json



class TaskManager:
#should be able to add a task
# should be able to finish a task
# write the tasks to a file for persistence
# read from the file: write every time there is
#                     an update, but read only once
#                     Initially, do a direct object dump

    def __init__(self, fileName=None):
        try:
            input = open(fileName, 'rb')
            self.tasks = pickle.load(input)
            self.fileName = fileName
        except:
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
        self.writeToFile(self.fileName)
    
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

    def finishTask(self):
        deb('finishTask: to delete::'+ str(args.id))
        self.tasks.delete(int(args.id))
        self.writeToFile(self.fileName)

    def createArgsObj(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser.add_argument('--task_dir')

        # add 'add' as a subparser
        add = subparsers.add_parser("add")
        add.add_argument('allPropVal', nargs='*')
        add.set_defaults(func=taskManager.add)

        # add 'fin' as a subparser
        fin = subparsers.add_parser("fin")
        fin.add_argument('id')
        fin.set_defaults(func=taskManager.finishTask)

        # add 'list' as a subparser
        lst = subparsers.add_parser("list")
        lst.set_defaults(func=taskManager.display)

        return parser.parse_args()

    def createDict(self, obj):

        deb('createDict for obj id= ' + str(obj.id))
        if obj is None:
            return {}

        resDict = {}
        objDict = {}
        objDict['children'] = [cObj.id for cObj in obj.children] if obj.children is not None else []
        objDict['parentId'] = obj.parent.id if obj.parent is not None else 0
        objDict['prop'] = obj.prop
        resDict[obj.id] = objDict
        
        if obj.children is not None:
            for childObj in obj.children:
                cDict = self.createDict(childObj)
                resDict.update(cDict)
        return resDict
        
    

    def writeToFile(self, fileName):
        with open(fileName, 'wb') as output:
            pickle.dump(self.tasks, output, -1)

        with open('newf.json','wb') as output:
            json.dump(self.tasks, output, default=self.createDict)

                
taskManager = TaskManager('taskObj')

args = taskManager.createArgsObj()
args.func()


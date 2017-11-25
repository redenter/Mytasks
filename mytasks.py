from tree import Tree; 
from tree import deb
from pprint import pprint
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
            self.tasks = self.readFromFile(fileName)
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
               newId = (val) 
            elif (key == 'parent'):
               parentId = int(val)
           
        if newId is None:
            # create a new id for the task
            newId = self.createId()
        else:
            # delete the key, value pair from the dictionary
            del prop['id']

        if parentId is not None:
            del prop['parent']

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
        with open(fileName,'wb') as output:
            json.dump(self.tasks, output, default=self.createDict)

    def str_hook(self, obj):
        if isinstance(obj, dict):
            return {k.encode('utf-8') if isinstance(k, unicode) else k :
                    self.str_hook(v)
                    for k,v in obj.items()}
        else:
            return obj.encode('utf-8') if isinstance(obj, unicode) else obj
        

    # read from json file.
    def readFromFile(self, filename):
        data = {}
        with open(filename, 'rb') as output:
            data = json.loads(output.read(), object_hook=self.str_hook)

        deb('readFromFile: keys are = ' + str(data.keys()))
        if data == {}:
            raise Exception('could not read Json file, or the file was empty!')


        resDict = {}
        parentId = -1
        for key, value in data.items():
            deb('readFromFile: key is = ' + key)
            deb('readFromFile: value is = ' + str(value))
            t = Tree(id=int(key))
            # if resDict has the object already use that
            if int(key) in resDict:
                t = resDict[int(key)]

            # set the other properties
            t.prop = value['prop']
            if int(value['parentId']) != int(key):
                if int(value['parentId']) in resDict:
                    parent = resDict[int(value['parentId'])]
                    t.parent = parent
                    parent.children.append(t)
                else:
                    resDict[int(value['parentId'])] = Tree(int(value['parentId']))
                    resDict[int(value['parentId'])].children.append(t)
            else:
                t.parent = t
                parentId = int(value['parentId'])

            resDict[int(key)] = t

        if parentId == -1:
            raise Exception('no top level task present in the json file')

        deb('readFromFile: the final dict file is ' + str(self.createDict(resDict[parentId])))
        return resDict[parentId]
    

taskManager = TaskManager('newf.json')
args = taskManager.createArgsObj()
args.func()


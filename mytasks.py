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
# should display tasks
# should be able to update tasks

    def __init__(self, fileName=None):
        try:
            self.tasks = self.readFromFile(fileName)
            self.fileName = fileName
        except:
            self.tasks = Tree(0)

    def createId(self):
        return str(random.randint(1, 20000))
    
    def getPropDictFromCL(self):
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
            deb('getPropDictFromCL:: prop= '+p+' val= '+v)
        return prop

    def add(self):
        prop = self.getPropDictFromCL()
        self.addTask(prop)

    # right now update appends prop dicts, replacing the old ones with the new values wherever there
    # is a clash. 
    # TODO: add optional parameters to completely replace the existing parameters
    def updateTask(self):
        prop = self.getPropDictFromCL()
        deb('updateTask: got::'+str(prop))
        if 'id' not in prop:
            raise Exception('no task id provided for update. Try add or provide the task id')

        currTask = self.tasks.find(prop['id']) 
        del prop['id']

        # need to change links if parent also needs to be updated
        if 'parent' in prop:
            deb('updateTask: parent in input prop. New parent id is::'+ prop['parent'])
            currParent = currTask.parent
            deb('updateTask: current parent is:'+currParent.id)
            newParentId = prop['parent']
            
            if newParentId != currParent.id:
                if newParentId == currTask.id:
                    newParentId = 0
                
                newParent = self.tasks.find(newParentId)

                if newParent is not None:
                    currParent.children.remove(currTask)

                    # we don't append in children list if the new parent is the current task
                    # but that condition is checked before we reach here so don't need an if condition
                    newParent.children.append(currTask)
                    currTask.parent = newParent
            del prop['parent']

        deb('updateTask: before currTask prop'+ str(currTask.prop))
        currTask.prop.update(prop)
        deb('updateTask: after currTask'+ str(currTask.prop))
        self.writeToFile(self.fileName)




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

        deb('addTask: creating new task with id =' + newId)

        if parentId is not None:
            deb('addTask: input parentId = ' + parentId)
            del prop['parent']

        task = Tree(id=newId, prop=prop)
        deb('addTask: created task object. Now inserting it into the tree')
        tasks.insert(task, parentId)
        self.writeToFile(self.fileName)
    
    def finishTask(self):
        deb('finishTask: to delete::'+ str(args.id))
        self.tasks.delete(args.id)
        self.writeToFile(self.fileName)

    def display(self):
        self.tasks.display()

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

        # add 'update' as a subparser
        upd = subparsers.add_parser("update")
        upd.add_argument('allPropVal', nargs='*')
        upd.set_defaults(func=taskManager.updateTask)

        # add 'list' as a subparser
        lst = subparsers.add_parser("list")
        lst.set_defaults(func=taskManager.display)

        return parser.parse_args()

    def createDict(self, obj):
        deb('createDict for taskId= ' + str(obj.id))
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
        deb('createDict: taskId' + str(obj.id) + ', final dictionary object is:' + str(resDict))
        return resDict
        

    def writeToFile(self, fileName):
        with open(fileName,'wb') as output:
            json.dump(self.tasks, output, default=self.createDict)

    # Decode the dict object obtained from json file and convert it into Tree object
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
            t = Tree(id=key)
            # if resDict has the object already use that
            if key in resDict:
                t = resDict[key]

            # set the other properties
            t.prop = value['prop']
            if str(value['parentId']) != str(key):
                deb('readFromFile: ParentId = ' + value['parentId'] +', key:'+ key)
                if value['parentId'] in resDict:
                    deb('readFromFile: key=' + key + ', parentId in resDict. ParentId:'+value['parentId'])
                    parent = resDict[value['parentId']]
                    t.parent = parent
                    parent.children.append(t)
                else:
                    deb('readFromFile: key=' + key + ', parentId not in resDict. ParentId:'+value['parentId'])
                    pTree = Tree(value['parentId'])
                    t.parent = pTree
                    pTree.children.append(t)
                    resDict[value['parentId']] = pTree
            else:
                deb('readFromFile: found root. ParentId = ' + value['parentId'] +', key:'+ key)
                t.parent = t
                parentId = value['parentId']

            resDict[key] = t

        if parentId == -1:
            raise Exception('no top level task present in the json file')

        deb('readFromFile: the final dict file is ' + str(self.createDict(resDict[parentId])))
        return resDict[parentId]
    

taskManager = TaskManager('newf.json')
args = taskManager.createArgsObj()
args.func()


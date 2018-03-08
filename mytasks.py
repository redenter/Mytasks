from tree import Tree; 
from tree import deb
from pprint import pprint
import argparse;
import random;
import cPickle as pickle
import copy
import json
import textwrap
from itertools import izip_longest as zip_longest
import datetime


class TaskManager:
#should be able to add a task
# should be able to finish a task
# write the tasks to a file for persistence
# read from the file: write every time there is
#                     an update, but read only once
# should display tasks
# should be able to update tasks

    def __init__(self, fileName=None):

        fileName = 'tasks.json' if fileName is None else fileName
        # get the args object
        self.args = self.createArgsObj()
        self.conf = self.getDefaultConf()
        self.fileName = (self.args.task_dir if self.args.task_dir is not None else '') + fileName

        #we want exception to be handled only when reading the file. Exceptions above 
        # would be because of a code error and not input.
        try:
            self.tasks = self.readFromFile(self.fileName)
        except:
            self.tasks = Tree(0)

    def createId(self):
        return str(random.randint(1, 20000))
    
    def getDefaultConf(self):
        conf = {}
        conf['displayList'] = [('Task Id', 10), ('Parent Id', 10), ('Task Description', 40), ('Project', 20), 
                            ('Tag', 20), ('Subtasks', 8)]
        conf['maxDisplay'] = 40
        return conf


    # decode the properties provided as command line input
    def getPropDictFromCL(self, clInputList, currProp='desc'):
        prop = {} 
        if clInputList is None:
            return prop

        newVal = ''
        elem = ''
        for elem in clInputList:
            pos = elem.find(':') 
            if pos == -1:
                newVal = newVal + ' ' + elem
            else:
                if newVal != '' :
                    if currProp is None or currProp == '':
                        raise Exception('property not provided')
                    prop[currProp.strip()] = newVal.strip()
                currProp = elem[:pos]
                newVal = elem[pos+1:]

        if newVal != '' :
            if currProp is None or currProp == '':
                raise Exception('property not provided')
            prop[currProp.strip()] = newVal.strip()

        return prop

    def add(self):
        prop = self.getPropDictFromCL(clInputList=args.allPropVal)
        if prop == {}:
            raise Exception('improper arguments')
        
        for p,v in prop.items():
            deb('add:: prop= '+p+' val= '+v)
        self.addTask(prop)

    # right now update appends prop dicts, replacing the old ones with the new values wherever there
    # is a clash. 
    # TODO: add optional parameters to completely replace the existing parameters
    def updateTask(self):
        prop = self.getPropDictFromCL(clInputList=args.allPropVal, currProp='id')

        if prop == {}:
            raise Exception('improper arguments')

        deb('updateTask: got::'+str(prop))
        if 'id' not in prop:
            raise Exception('no task id provided for update. Try add or provide the task id')

        currTask = self.tasks.find(prop['id']) 
        del prop['id']

        # need to change links if parent also needs to be updated
        if 'parent' in prop:
            deb('updateTask: parent in input prop. New parent id is::'+ prop['parent'])
            currParent = currTask.parent
            deb('updateTask: current parent is:'+ str(currParent.id))
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
        prop['completed'] = 0
        task = Tree(id=newId, prop=prop)
        deb('addTask: created task object. Now inserting it into the tree')
        tasks.insert(task, parentId)
        self.writeToFile(self.fileName)
    
    def finishTask(self):
        deb('finishTask: to delete::'+ str(args.id))
        self.tasks.addPropToSubtree(args.id, {'completed':1, 'completion_time':str(datetime.datetime.now())})
        #self.tasks.delete(args.id)
        self.writeToFile(self.fileName)

    def formatTask(self, strList, widthList,initIndent=2, separation=4):
        wrList=[]
        #print strList
        for i, el in enumerate(strList):
            wrList.append(textwrap.wrap(el, width=widthList[i]))
        
        #create format string
        fString = ' '*initIndent
        for i,val in enumerate(widthList):
            fString += '{'+str(i)+':'+str(val)+'}' + ' '*separation

        #print fString

        results = []
        for z in zip_longest(*wrList, fillvalue=''):
            results.append(fString.format(*z))
        return '\n'.join(results)

    def passesFilter(self, task, filters):
      if task.prop is not None and task.prop != {}:
          fullProp = {}
          fullProp['id'] = str(task.id)
          fullProp['parent'] = str(task.parent.id) if task.parent is not None else ''
          fullProp.update(task.prop)

          if(filters == {}):
             return True
          for k,v in filters.items():
              if k not in fullProp:
                  return False
              if v == fullProp[k] or v == str(fullProp[k]):
                  return True
              else:
                  if k not in ('id', 'completed', 'parent') and v in fullProp[k]:
                      return True
                  return False
      else:
          return False


          

    def displayAll(self):            
        filt = self.getPropDictFromCL(clInputList=args.filters, currProp='project')
        if args.completed:
            filt.update({'completed':1})
            self.display(filters=filt)
        else:
            filt.update({'completed':0})
            self.display(filters=filt)
            if args.include_completed:
                filt.update({'completed':1})
                print '\n'
                print 'Completed Tasks'
                self.display(filters = filt)
                
    def display(self, filters, tasks=None, level=0):

        strNameList = []
        widthList = []
        for (strName, strLength) in self.conf['displayList']:
            strNameList.append(strName)
            widthList.append(strLength)

        if tasks is None:
            print '\n'
            print self.formatTask(strNameList, widthList)
            print ''

            t = self.tasks
        else:
            t = tasks

        if self.passesFilter(t, filters) and t.id != 0:
            strList = [str(t.id), str(t.parent.id), 
                       t.prop['desc'] if 'desc' in t.prop else '', 
                       t.prop['project'] if 'project' in t.prop else '',
                       t.prop['tag'] if 'tag' in t.prop else '',
                       str(len(t.children)) if t.children is not None else 0 ]
            widthList = [10,10,40,20,20,8]
            print self.formatTask(strList, widthList)
            print ''

        if args.level is not None:
            if int(args.level) <= level:
                return

        level += 1

        for ch in t.children:
            self.display(tasks = ch, filters= filters, level = level)

         
        #self.tasks.display()

    def createArgsObj(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser.add_argument('--task_dir')

        # add 'add' as a subparser
        add = subparsers.add_parser("add")
        add.add_argument('allPropVal', nargs='*')
        add.set_defaults(func=self.add)

        # add 'fin' as a subparser
        fin = subparsers.add_parser("fin")
        fin.add_argument('id')
        fin.set_defaults(func=self.finishTask)

        # add 'update' as a subparser
        upd = subparsers.add_parser("update")
        upd.add_argument('allPropVal', nargs='*')
        upd.set_defaults(func=self.updateTask)

        # add 'list' as a subparser
        lst = subparsers.add_parser("list")
        lst.add_argument('-f','--filters', nargs='*')
        lst.add_argument('-l','--level', help='list tasks only up to the specified depth. For example, if level = 1 only the top level tasks will be displayed.' )
        lst.add_argument('-comp', '--completed',action='store_true')
        lst.add_argument('-incHist', '--include_completed',action='store_true')
        lst.set_defaults(func=self.displayAll)

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
        if 'completed' not in objDict['prop']:
            objDict['prop']['completed'] = 0
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
                    self.str_hook(v) for k,v in obj.items()}
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
        parentId = ''
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
                deb('readFromFile: ParentId = ' + str(value['parentId'])+', key:'+ str(key))
                if value['parentId'] in resDict:
                    deb('readFromFile: key=' + str(key) + ', parentId in resDict. ParentId:'+ str(value['parentId']))
                    parent = resDict[value['parentId']]
                    t.parent = parent
                    parent.children.append(t)
                else:
                    deb('readFromFile: key=' + str(key) + ', parentId not in resDict. ParentId:'+ str(value['parentId']))
                    pTree = Tree(value['parentId'])
                    t.parent = pTree
                    pTree.children.append(t)
                    resDict[value['parentId']] = pTree
            else:
                deb('readFromFile: found root. ParentId = ' + str(value['parentId']) +', key:'+ str(key))
                t.parent = t
                parentId = value['parentId']

            resDict[key] = t

        if parentId == '':
            raise Exception('no top level task present in the json file')

        deb('readFromFile: the final dict file is ' + str(self.createDict(resDict[parentId])))
        return resDict[parentId]
    

taskManager = TaskManager('newf.json')
args = taskManager.args
args.func()


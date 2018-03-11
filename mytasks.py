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

        #new Tasks obj
        self.tasksObj = Tasks()

    def createId(self):
        return str(random.randint(1, 20000))
    
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

        newId = self.createId()
        parentId = 0
        if 'id' in prop:
            newId = prop['id']
            del prop['id']

        if 'parent' in prop:
            newId = prop['parent']
            del prop['parent']

        for key, val in prop.items():
            # display key value pairs provided
            deb('add:: prop= '+p+' val= '+v)
           
        self.tasksObj.addTask(newId, parentId, prop)
        # update the file 
        self.writeToFile(self.fileName)

    # right now update appends prop dicts, replacing the old ones with the new values wherever there
    # is a clash. 
    # TODO: add optional parameters to completely replace the existing parameters
    def update(self):
        prop = self.getPropDictFromCL(clInputList=args.allPropVal, currProp='id')

        if prop == {}:
            raise Exception('improper arguments')

        deb('update: got::'+str(prop))
        if 'id' not in prop:
            raise Exception('no task id provided for update. Try add or provide the task id')

        taskId = prop['id']
        del prop['id']

        parentId = None
        if 'parent' in prop:
            parentId = prop['parent']
            del prop['parent']

        self.tasksObj.updateTask(taskId, parentId, prop)

        # need to change links if parent also needs to be updated
        self.writeToFile(self.fileName)

    def finishTask(self):
        deb('finishTask: to archive::'+ str(args.id))
        self.tasksObj.archiveTask(args.id)
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
        upd.set_defaults(func=self.update)

        # add 'list' as a subparser
        lst = subparsers.add_parser("list")
        lst.add_argument('-f','--filters', nargs='*')
        lst.add_argument('-l','--level', help='list tasks only up to the specified depth. For example, if level = 1 only the top level tasks will be displayed.' )
        lst.add_argument('-comp', '--completed',action='store_true')
        lst.add_argument('-incHist', '--include_completed',action='store_true')
        lst.set_defaults(func=self.displayAll)

        return parser.parse_args()


    def writeToFile(self, fileName):
        with open(fileName,'wb') as output:
            json.dump(self.tasks, output, default=self.tasksObj.createDict)

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

        deb('readFromFile: the final dict file is ' + str(self.tasksObj.createDict(resDict[parentId])))
        return resDict[parentId]
    

taskManager = TaskManager('newf.json')
args = taskManager.args
args.func()


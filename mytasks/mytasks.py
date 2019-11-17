from tree import Tree; 
from tree import deb
from tasks import Tasks
from pprint import pprint
import argparse;
import copy
import textwrap
import datetime
from itertools import izip_longest as zip_longest

class MyTasksCLI:
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
        tasks_dir = self.args.task_dir;

        self.tasks = Tasks(fileName, tasks_dir)

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

        lst.add_argument('-l','--level', 
                         help='list tasks only up to the specified depth.' + 
                              ' For example, if level = 1 only the top level' + 
                              ' tasks will be displayed.' )

        lst.add_argument('-comp', '--completed',action='store_true')
        lst.add_argument('-incHist', '--include_completed',action='store_true')
        lst.set_defaults(func=self.displayAll)

        return parser.parse_args()

    def add(self):
        prop = self.getPropDictFromCL(clInputList=args.allPropVal)
        if prop == {}:
            raise Exception('improper arguments')

        if 'id' in prop:
            newId = prop['id']
            del prop['id']
        else:
            newId = None

        if 'parent' in prop:
            parentId = prop['parent']
            del prop['parent']
        else:
            parentId = None

        for key, val in prop.items():
            # display key value pairs provided
            deb('add:: prop= '+ key +' val= ' + val)
           
        self.tasks.addTask(newId, parentId, prop)

    
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

        self.tasks.updateTask(taskId, parentId, prop)

    def finishTask(self):
        deb('finishTask: to archive::'+ str(args.id))
        self.tasks.archiveTask(args.id)



############## Command line display ###########################
    def getDefaultConf(self):
        conf = {}
        conf['displayList'] = [('Task Id', 10), ('Parent Id', 10), \
                               ('Task Description', 40), ('Project', 20), \
                               ('Tag', 20), ('Subtasks', 8)]
        conf['maxDisplay'] = 40
        return conf

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

            t = self.tasks.taskObj
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
#
#
#
#        
#
#
myTasksCLI = MyTasksCLI('newf.json')
args = myTasksCLI.args
args.func()
#

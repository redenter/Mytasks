from tree import Tree; 
from tree import deb

# A collection of tasks 
# Instances of this class should be able to add a task
# to the collection, delete it, update it and provide a list or a subset of
# collection for display
class Tasks:
    ROOT_TASK_ID = 0
    def __init__(self, tasksObj=None):
        if tasksObj is not None:
            self.tasks = tasksObj.tasks
        else:
            self.tasks = Tree(Tasks.ROOT_TASK_ID)

# create a tree obj based on the input prop and val and insert
    def addTask(self, taskId, parentTaskId, prop):
        tasks = self.tasks
        if taskId is None or taskId <= Tasks.ROOT_TASK_ID:
            raise Exception('Cannot create task with taskId ' + taskId);
        if parentTaskId is None or parentTaskId < Tasks.ROOT_TASK_ID:
            raise Exception('Cannot create task with parentTaskId ' + parentTaskId);

        deb('Tasks: addTask- creating new task with id =' + str(taskId) +
            ', parent task id =' + str(parentTaskId));

        prop['completed'] = 0
        task = Tree(id=taskId, prop=prop)
        deb('Tasks: addTask- created task object. Now inserting it into the tree')
        tasks.insert(task, parentTaskId)

# update a task
    def updateTask(self, taskId, prop = None, parentId = None, updateSubtasks = False):
        if taskId == Tasks.ROOT_TASK_ID:
            raise Exception('Cannot update task with taskId: ' + taskId);

        # raise an exception if not found
        currTask = self.tasks.find(taskId)
        if currTask is None:
            raise Exception('Cannot find task with task id = ' + taskId);
        
        if self.__isArchived(currTask):
            raise Exception('Cannot update archived task')

        # nothing to update 
        if prop is None and parentId is None:
            return

        if parentId is not None:
            deb('Tasks: updateTask- new parent id is: '+ parentId)
            currParent = currTask.parent
            deb('updateTask: current parent is:'+ str(currParent.id))
            
            if parentId != currParent.id:
                if parentId == currTask.id:
                    newParentId = Tasks.ROOT_TASK_ID
                
                newParent = self.tasks.find(parentId)

                if newParent is not None:
                    currParent.children.remove(currTask)

                    # we don't append in children list if the new parent is the current task
                    # but that condition is checked before we reach here so don't need an if condition
                    newParent.children.append(currTask)
                    currTask.parent = newParent

        if prop is not None:
            deb('Tasks - updateTask: before updating currTask prop '+ str(currTask.prop))
            if updateSubtasks:
                self.__updateSubtasks(currTask, prop)
            else:
                currTask.prop.update(prop)

            deb('Tasks - updateTask: after updating currTask prop'+ str(currTask.prop))
 
    def archiveTask(self, taskId):
        task = self.tasks.find(taskId)
        if task is None:
            raise Exception('Could not find task with task id :' + taskId) 
 
        if self.__isArchived(task):
            return
        completionDict = {'completed':1, 'completion_time':str(datetime.datetime.now())}
        self.__updateSubtasks(task, completionDict)

        
    # this routine updates the task and all associated subtasks with the provided properties
    def __updateSubtasks(self, currTask, prop):
        currTask.prop.update(prop)

        for ch in currTask.children:
            self.__updateSubtasks(ch.id, prop)
    
    # is completed
    def __isArchived(self, task):
        if 'completed' not in task.prop:
            return false
        return task.prop['completed'] == 1
            
    def createDict(self):
        return self.__createDictForTask(self.tasks)

    # create an object dictionary
    # similar to a serialization operation
    def __createDictForTask(self, tasks):
        if tasks is None:
            return {} 
        deb('Tasks: createDict for taskId= ' + str(tasks.id))


        resDict = {}
        tasksDict = {}
        tasksDict['children'] = [cObj.id for cObj in tasks.children] if tasks.children is not None else []
        tasksDict['parentId'] = tasks.parent.id if tasks.parent is not None else Tasks.ROOT_TASK_ID
        tasksDict['prop'] = tasks.prop
        if 'completed' not in tasksDict['prop']:
            tasksDict['prop']['completed'] = 0
        resDict[tasks.id] = tasksDict
        
        if tasks.children is not None:
            for childObj in tasks.children:
                cDict = self.__createDictForTask(childObj)
                resDict.update(cDict)
        deb('Tasks: createDict- taskId' + str(tasks.id) + ', final dictionary is:' + str(resDict))
        return resDict
    
    # create a tasks object from a dictionary
    # we expect the dictionary to be in a certain way. 
    # Need some checks in place to make sure that is obeyed
    def buildFromDict(self, inputDict):
        if inputDict == {}:
            raise Exception('could not read Json file, or the file was empty!')

        resDict = {}
        parentId = ''
        for key, value in inputDict.items():
            deb('buildFromDict: key is = ' + key)
            deb('buildFromDict: value is = ' + str(value))
            t = Tree(id=key)
            # if resDict has the object already use that
            if key in resDict:
                t = resDict[key]

            # set the other properties
            t.prop = value['prop']
            if str(value['parentId']) != str(key):
                deb('buildFromDict: ParentId = ' + str(value['parentId'])+', key:'+ str(key))
                if value['parentId'] in resDict:
                    deb('buildFromDict: key=' + str(key) + ', parentId in resDict. ParentId:'+ str(value['parentId']))
                    parent = resDict[value['parentId']]
                    t.parent = parent
                    parent.children.append(t)
                else:
                    deb('buildFromDict: key=' + str(key) + ', parentId not in resDict. ParentId:'+ str(value['parentId']))
                    pTree = Tree(value['parentId'])
                    t.parent = pTree
                    pTree.children.append(t)
                    resDict[value['parentId']] = pTree
            else:
                deb('buildFromDict: found root. ParentId = ' + str(value['parentId']) +', key:'+ str(key))
                t.parent = Tasks.ROOT_TASK_ID
                parentId = value['parentId']

            resDict[key] = t

        if parentId == '':
            raise Exception('no top level task present in the json file')
        return resDict[parentId]

    # read from json file.
    def readFromFile(self, filename):
        data = {}
        with open(filename, 'rb') as output:
            data = json.loads(output.read(), object_hook=self.str_hook)

        deb('readFromFile: keys are = ' + str(data.keys()))
        if data == {}:
            raise Exception('could not read Json file, or the file was empty!')
        return self.buildFromDict(data)

    # Decode the dict object obtained from json file and convert it into Tree object
    def str_hook(self, obj):
        if isinstance(obj, dict):
            return {k.encode('utf-8') if isinstance(k, unicode) else k :
                    self.str_hook(v) for k,v in obj.items()}
        else:
            return obj.encode('utf-8') if isinstance(obj, unicode) else obj

    def writeToFile(self, fileName):
        with open(fileName,'wb') as output:
            json.dump(self.tasks, output, default=self.tasksObj.createDict)

    # read from json file.
#    def readFromFile(self, filename):
#        data = {}
#        with open(filename, 'rb') as output:
#            data = json.loads(output.read(), object_hook=self.str_hook)
#
#        deb('readFromFile: keys are = ' + str(data.keys()))
#        if data == {}:
#            raise Exception('could not read Json file, or the file was empty!')
#
#        resDict = {}
#        parentId = ''
#        for key, value in data.items():
#            deb('readFromFile: key is = ' + key)
#            deb('readFromFile: value is = ' + str(value))
#            t = Tree(id=key)
#            # if resDict has the object already use that
#            if key in resDict:
#                t = resDict[key]
#
#            # set the other properties
#            t.prop = value['prop']
#            if str(value['parentId']) != str(key):
#                deb('readFromFile: ParentId = ' + str(value['parentId'])+', key:'+ str(key))
#                if value['parentId'] in resDict:
#                    deb('readFromFile: key=' + str(key) + ', parentId in resDict. ParentId:'+ str(value['parentId']))
#                    parent = resDict[value['parentId']]
#                    t.parent = parent
#                    parent.children.append(t)
#                else:
#                    deb('readFromFile: key=' + str(key) + ', parentId not in resDict. ParentId:'+ str(value['parentId']))
#                    pTree = Tree(value['parentId'])
#                    t.parent = pTree
#                    pTree.children.append(t)
#                    resDict[value['parentId']] = pTree
#            else:
#                deb('readFromFile: found root. ParentId = ' + str(value['parentId']) +', key:'+ str(key))
#                t.parent = t
#                parentId = value['parentId']
#
#            resDict[key] = t
#
#        if parentId == '':
#            raise Exception('no top level task present in the json file')
#
#        deb('readFromFile: the final dict file is ' + str(self.tasksObj.createDict(resDict[parentId])))
#        return resDict[parentId]
#



t = Tasks()
t.addTask(10,0,{})
t.addTask(11,10,{})
t.updateTask(taskId = 10, prop={'test':1})
print t.createDict()
t.archiveTask(10)
print t.createDict()

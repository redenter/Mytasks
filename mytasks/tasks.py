from tree import Tree; 
from tree import deb
import datetime
from fileDB import FileDB
import random;

# A collection of tasks 
# Instances of this class should be able to add a task
# to the collection, delete it, update it and provide a list or a subset of
# collection for display
class Tasks:
    ROOT_TASK_ID = 0
    def __init__(self, fileName=None, task_dir=None):
        try:
            if fileName is not None:
                task_dir = task_dir if task_dir is not None else ''
                self.fileName = task_dir + fileName
                self.fileDB = FileDB(self.fileName)
                self.taskObj = self.read()
            else:
                self.taskObj = Tree(Tasks.ROOT_TASK_ID)
                self.fileName = None
        except:
            self.taskObj = Tree(Tasks.ROOT_TASK_ID)

    def createId(self):
        return str(random.randint(1, 20000))

# create a tree obj based on the input prop and val and insert
    def addTask(self, taskId=None, parentTaskId=None, prop=None):
        if taskId is None:
            taskId = self.createId()
        elif taskId <= Tasks.ROOT_TASK_ID:
            raise Exception('Cannot create task with taskId ' + str(taskId));

        if parentTaskId is None:
            parentTaskId = Tasks.ROOT_TASK_ID
        elif parentTaskId < Tasks.ROOT_TASK_ID:
            raise Exception('Cannot create task with parentTaskId ' + 
                            str(parentTaskId));

        if prop is None:
            prop = {}

        deb('Tasks: addTask- creating new task with id =' + str(taskId) +
            ', parent task id =' + str(parentTaskId));

        prop['completed'] = 0
        task = Tree(id=taskId, prop=prop)
        deb('Tasks: addTask- created task object. ' +
            'Now inserting it into the tree')
        self.taskObj.insert(task, parentTaskId)

        # update the file 
        self.write()

    # create a tasks object from a dictionary
    # we expect the dictionary to be in a certain way. 
    # Need some checks in place to make sure that is obeyed
    def dictToTask(self, inputDict):
        if inputDict == {}:
            raise Exception('could not read Json file, or the file was empty!')

        resDict = {}
        parentId = ''
        for key, value in inputDict.items():
            deb('dictToTask: key is = ' + str(key))
            deb('dictToTask: value is = ' + str(value))
            t = Tree(id=key)
            # if resDict has the object already use that
            if key in resDict:
                t = resDict[key]

            # set the other properties
            t.prop = value['prop']
            if str(value['parentId']) != str(key):
                deb('dictToTask: ParentId = ' + 
                    str(value['parentId']) + ', key:' + str(key))

                if value['parentId'] in resDict:
                    deb('dictToTask: key=' + str(key) + 
                        ', parentId in resDict. ParentId:'+ str(value['parentId']))
                    parent = resDict[value['parentId']]
                    t.parent = parent
                    parent.children.append(t)
                else:
                    deb('dictToTask: key=' + str(key) + 
                        ', parentId not in resDict. ParentId:' + 
                        str(value['parentId']))
                    pTree = Tree(value['parentId'])
                    t.parent = pTree
                    pTree.children.append(t)
                    resDict[value['parentId']] = pTree
            else:
                deb('dictToTask: found root. ParentId = ' + 
                    str(value['parentId']) +', key:'+ str(key))
                t.parent = t
                parentId = value['parentId']

            resDict[key] = t

        if parentId == '':
            raise Exception('no top level task present in the json file')
        return resDict[parentId]


    # read from json file.
    def read(self):
        if self.fileName is None:
            return
        data = self.fileDB.readAll()
        return self.dictToTask(data)

    # create an object dictionary
    # similar to a serialization operation
    def taskToDict(self, tasks):
        if tasks is None:
            return {} 
        deb('Tasks: createDict for taskId= ' + str(tasks.id))

        resDict = {}
        tasksDict = {}
        tasksDict['children'] = [cObj.id for cObj in tasks.children] \
                                if tasks.children is not None else []
        tasksDict['parentId'] = tasks.parent.id if tasks.parent is not None \
                                else Tasks.ROOT_TASK_ID
        tasksDict['prop'] = tasks.prop
        if 'completed' not in tasksDict['prop']:
            tasksDict['prop']['completed'] = 0
        resDict[tasks.id] = tasksDict
        
        if tasks.children is not None:
            for childObj in tasks.children:
                cDict = self.taskToDict(childObj)
                resDict.update(cDict)
        deb('Tasks: createDict- taskId' + str(tasks.id) + 
            ', final dictionary is:' + str(resDict))
        return resDict

    def write(self):
        if self.fileName is None:
            return
        taskDict = self.taskToDict(self.taskObj)
        self.fileDB.writeAll(taskDict)










# update a task
#    def updateTask(self, taskId, prop = None, parentId = None, 
#                   updateSubtasks = False):
#        if taskId == Tasks.ROOT_TASK_ID:
#            raise Exception('Cannot update task with taskId: ' + taskId);
#
#        # raise an exception if not found
#        currTask = self.tasks.find(taskId)
#        if currTask is None:
#            raise Exception('Cannot find task with task id = ' + taskId);
#        
#        if self.__isArchived(currTask):
#            raise Exception('Cannot update archived task')
#
#        # nothing to update 
#        if prop is None and parentId is None:
#            return
#
#        if parentId is not None:
#            deb('Tasks: updateTask- new parent id is: ' + str(parentId))
#            currParent = currTask.parent
#            deb('updateTask: current parent is:' + str(currParent.id))
#            
#            if parentId != currParent.id:
#                if parentId == currTask.id:
#                    newParentId = Tasks.ROOT_TASK_ID
#                
#                newParent = self.tasks.find(parentId)
#
#                if newParent is not None:
#                    currParent.children.remove(currTask)
#
#                    # we don't append in children list if the new parent is 
#                    # the current task but that condition is checked before 
#                    # we reach here so don't need an if condition
#                    newParent.children.append(currTask)
#                    currTask.parent = newParent
#
#        if prop is not None:
#            deb('Tasks - updateTask: before updating currTask prop ' + 
#                str(currTask.prop))
#            if updateSubtasks:
#                self.__updateSubtasks(currTask, prop)
#            else:
#                currTask.prop.update(prop)
#
#            deb('Tasks - updateTask: after updating currTask prop' + 
#                str(currTask.prop))
# 
#       
#    # this routine updates the task and all associated subtasks 
#    # with the provided properties
#    def __updateSubtasks(self, currTask, prop):
#        currTask.prop.update(prop)
#
#        for ch in currTask.children:
#            self.__updateSubtasks(ch.id, prop)
#
#    def archiveTask(self, taskId):
#        task = self.tasks.find(taskId)
#        if task is None:
#            raise Exception('Could not find task with task id :' + taskId) 
# 
#        if self.__isArchived(task):
#            return
#        completionDict = {'completed':1, 
#                          'completion_time':str(datetime.datetime.now())}
#        self.__updateSubtasks(task, completionDict)
#
#    # is completed
#    def __isArchived(self, task):
#        if 'completed' not in task.prop:
#            return false
#        return task.prop['completed'] == 1
#            
    




#t = Tasks()
#t.addTask(10,0,{})
#t.addTask(11,10,{})
#t.updateTask(taskId = 10, prop={'test':1})
#print t.createDict()
#t.archiveTask(10)
#print t.createDict()

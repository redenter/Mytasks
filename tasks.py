
# A collection of tasks 
# Instances of this class should be able to add a task
# to the collection, delete it, update it and provide a list or a subset of
# collection for display
class Tasks:
    def __init__(self, tasksObj=None):
        if tasksObj is not None:
            self.tasks = tasksObj.tasks
        else:
            self.tasks = Tree(0)

# create a tree obj based on the input prop and val and insert
    def addTask(self, taskId, parentTaskId, prop):
        tasks = self.tasks
        if taskId is None or taskId <= 0:
            raise Exception('Cannot create task with taskId ' + taskId);
        if parentTaskId is None or parentTaskId < 0:
            raise Exception('Cannot create task with parentTaskId ' + parentTaskId);

        deb('Tasks: addTask- creating new task with id =' + taskId +
            ', parent task id =' + parentTaskId);

        prop['completed'] = 0
        task = Tree(id=taskId, prop=prop)
        deb('Tasks: addTask- created task object. Now inserting it into the tree')
        tasks.insert(task, parentTaskId)

# update a task
    def updateTask(self, taskId, prop = None, parentId = None, updateSubtasks = False):
        if taskId == 0:
            raise Exception('Cannot update task with taskId: ' + taskId);

        # raise an exception if not found
        currTask = self.tasks.find(taskId)
        if currTask is None:
            raise Exception('Cannot find task with task id = ' + taskId);
        
        if self.__isArchived(taskId):
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
                    newParentId = 0
                
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
    def __createDictForTask(self, tasks):
        if tasks is None:
            return {} 
        deb('Tasks: createDict for taskId= ' + str(tasks.id))


        resDict = {}
        tasksDict = {}
        tasksDict['children'] = [cObj.id for cObj in tasks.children] if tasks.children is not None else []
        tasksDict['parentId'] = tasks.parent.id if tasks.parent is not None else 0
        tasksDict['prop'] = tasks.prop
        if 'completed' not in tasksDict['prop']:
            tasksDict['prop']['completed'] = 0
        resDict[tasks.id] = tasksDict
        
        if tasks.children is not None:
            for childObj in tasks.children:
                cDict = self.__createDictForTask(childObj)
                resDict.update(cDict)
        deb('Tasks: createDict- taskId' + str(tasks.id) + ', final dictionary tasksect is:' + str(resDict))
        return resDict
    
    # create a tasks object from a dictionary
    #def buildFromDict(self, inputDict):



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


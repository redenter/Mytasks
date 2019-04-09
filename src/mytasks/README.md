# Mytasks - A command line task manager

Mytasks is a command line task manager. While there are a number of such tools available today, Mytasks provides certain functionalities which I struggled to find when I was searching for a tool. 

1. **Linking tasks** - With mytasks, you can add any number of subtasks to a given task. Although the goal of any todo list is to help *finish* tasks, you need some way to organize them when things get out of hand.

2. **Adding information** - Any number of details can be added to a given task in the form of key value pairs. Details like project, tag, parent task id, description are recognized and displayed by default. **Any** other details (priority, deadline etc) can be added by the user as per requirement. 

3.  **Easy installation** - This is a python based project and can be installed on any machine with Python 2.7 or higher. It takes less than a minute!

While taskwarrior would have sufficed for my requirements, I spent more time trying to install Taskwarrior in my work machine than I spent building mytasks.

## Getting Started


### Prerequisites

Mytasks requires python 2.7 or higher.  It works on Linux, OS X, and Windows (with Cygwin).

### Installing

Installing and setting up mytasks is simple. After downloading the source code, create a directory to store the tasks.

```
mkdir ~/tasksdir
```
Add the following alias in ~/.bashrc.

```
alias tasks='python <path_to_code>/mytasks.py 
             --task_dir /<home_dir>/mytasks/'
```
Finally, run

```
source ~/.bashrc
```


## Usage

 There are four main functionalities provided - add, list, update, fin.

###Add###
Each task in mytasks is stored in a tree structure. In other words, each task has a parent task, a dictionary containing key value pairs and a list of sub-tasks or child tasks.

To add a task, simply provide all the necessary key value pairs. No key is needed for task description. It will be stored in desc by default.

`tasks add <task-description> <other properties>`

Note: Any property apart from task id, parent task id , description, project name, tag name will not be displayed by the list functionality as of now, even though the key-value will be added to the task. The option to configure the display will be added in the upcoming release.

For e.g: 

1.

 `$ task add complete README for mytasks. project:mytasks ` 

To view the tasks

```
$ tasks list


  Task Id       Parent Id     Task Description                            project                 tag

  18550         0             complete README for mytasks                 mytasks
```

Note that, the parent of each task is 0 unless specified. In other words, task 0 is the 'root' task.

2.

```
$ tasks add complete usage section parent:18550 
	   tag:documentation, sample project:mytasks
```

```
$ tasks list


  Task Id       Parent Id     Task Description                            project                 tag

  18550         0             complete README for mytasks                 mytasks

  17031         18550         complete usage section                      mytasks                 documentation,
                                                                                                  sample
```	

3.

```
$ tasks add grow and sell potatoes, become a millionaire project:farming tag:sample expected_issues: don't have farmland.

$ tasks list


  Task Id       Parent Id     Task Description                            project                 tag

  16378         0             grow and sell potatoes, become a            farming                 sample
                              millionaire

  18550         0             complete README for mytasks                 mytasks

  17031         18550         complete usage section                      mytasks                 documentation,
                                                                                                  sample
```
###List###

As shown in the previous examples, to see all tasks simply type `tasks list`. Currently, this command displays the task id, parent task id, task description, project, tag and the number of sub-tasks. 
*Options to display other properties will be provided in the next release.*

The list of visible tasks can be trimmed based on two parameters.

1. **-f or --filters**: Filter the tasks based on any property or key-value pair.
	Note: the default key is project. For other keys, the key name has to be provided as well.

For e.g.

1. 

```
$ tasks list -f mytasks


  Task Id       Parent Id     Task Description                            project                 tag

  18550         0             complete README for mytasks                 mytasks

  17031         18550         complete usage section                      mytasks                 documentation,
                                                                                                  sample
                                                                                                  
```
Or,

```
$ tasks list -f tag:sample


  Task Id       Parent Id     Task Description                            project                 tag

  16378         0             grow and sell potatoes, become a            farming                 sample
                              millionaire

  17031         18550         complete usage section                      mytasks                 documentation,
                                                                                                  sample

```

2. **-l or --level**: This can be used to specify the depth upto which the tasks should be displayed. 
 Level 1 implies all first level tasks with parent=0.
 
 ```
 $ tasks list -l 1


  Task Id       Parent Id     Task Description                            project                 tag

  16378         0             grow and sell potatoes, become a            farming                 sample
                              millionaire

  18550         0             complete README for mytasks                 mytasks
```

Similarly, level 2 includes sub-tasks (or children) of the above tasks.



```
$ tasks list -l 2


  Task Id       Parent Id     Task Description                            project                 tag

  16378         0             grow and sell potatoes, become a            farming                 sample
                              millionaire

  18550         0             complete README for mytasks                 mytasks

  17031         18550         complete usage section                      mytasks                 documentation,
                                                                                                  sample
```


###Update###
To update a task
` tasks update <task_id> <updated key value pairs>`

The key value pairs mentioned in this command are added to the task if they are new. Otherwise, the existing values are replaced.

For example,

```
$ tasks update 16378 desc:grow and sell watermelons, become a billionaire tag:big plans

$ tasks list -f farming


  Task Id       Parent Id     Task Description                            project                 tag

  16378         0             grow and sell watermelons, become a         farming                 big plans
                              billionaire

```

###Fin###

To mark a task completed use `tasks fin <task_id> `
Currently, completed tasks are removed from the file as well. *An option to archive finished tasks will be provided in the next release.*
For example,

```
$ tasks fin 17031

$ tasks list

  Task Id       Parent Id     Task Description                            project                 tag

  16378         0             grow and sell watermelons, become a         farming                 big plans
                              billionaire

  18550         0             complete README for mytasks                 mytasks

```


## Acknowledgements
This project is heavily inspired by [sjl/t](https://github.com/sjl/t).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


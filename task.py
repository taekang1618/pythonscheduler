""" A Python Class for a Task object of the Scheduler.
They are simple objects with
  1. name(string)
  2. the amount of time it takes to finish the task(integer)
  3. description of the task(string)
  3. array of children tasks
  4. array of parent tasks
"""

from functools import total_ordering
from random import randint

@total_ordering
class Task(object):

    def __init__(self, name='default', time=0, description='', priority=1):
        ''' Initializes a task with name, time, and description.
        For default, name='default', time=0, and description=''.
        '''
        self.id = randint(1, 10000)
        self.name = name
        self.time = time
        self.description = description
        self.priority = priority
        # self.children = []
        # self.parents = []


    def __str__(self):
        ''' Outputs the name of the task '''
        return self.name


    def __lt__(self, other):
        return self.priority < other.priority


    def __eq__(self, other):
        return self.priority == other.priority and self.id == other.id


    def __hash__(self):
        return self.id


    # def addChild(self, child):
    #     ''' Adds a child task to the current task's children list
    #     if the child does not exist in the current children list.
    #     '''
    #     if child.name != self.name:
    #         if child not in self.children:
    #             self.children.append(child)
    #         else:
    #             print("Task already exists in children list!")
    #     else:
    #         print("Child name can't be same as parent name!")
    #
    #
    # def addChildren(self, children):
    #     ''' Add multiple children '''
    #     for c in children:
    #         self.addChild(c)
    #
    #
    # def removeChild(self, child_name):
    #     ''' Removes a child task from the current task's children list
    #     if the child name exists in the current children list.
    #     '''
    #     for c in self.children:
    #         if child_name == c.name:
    #             self.children.remove(c)
    #
    #
    # def addParent(self, parent):
    #     ''' Adds a parent task to the current task's parents list
    #     if the parent does not exist in the current parent list.
    #     '''
    #     if parent.name != self.name:
    #         if parent not in self.parents:
    #             self.parents.append(parent)
    #         else:
    #             print("Task already exists in parents list!")
    #     else:
    #         print("Parent name can't be same as child name!")
    #
    #
    # def addParents(self, parents):
    #     ''' Adds multiple parents '''
    #     for p in parents:
    #         self.addParent(p)
    #
    #
    # def removeParent(self, parent_name):
    #     ''' Removes a parent task from the current task's parents list
    #     if the parent name exists in the current parents list.
    #     '''
    #     for p in self.parents:
    #         if parent_name == p.name:
    #             self.parents.remove(p)


    def editDescription(self, new_description):
        ''' Edit description. '''
        self.description = new_description


    def addDescription(self, more_description):
        ''' Add more description to existing one. '''
        if self.description == '':
            self.description = more_description
        else:
            self.description = self.description + '/ ' + more_description


    def editTime(self, new_time):
        ''' Edit time. '''
        self.description = new_time


    def addTime(self, more_time):
        ''' Add time to current time. '''
        self.time += more_time


    def editPriority(self, new_pr):
        ''' Edit task priority. '''
        self.priority = new_pr


    def addTime(self, add_pr):
        ''' Add value to current priority. '''
        self.priority += add_pr

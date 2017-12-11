''' A Python Class for a scheduling tasks.
Tasks are represented in a directed acyclic graph.
Implements a custom scheduling algorithm using topological sort and priority
queues to optimize the amount of time it takes to finish all tasks.
'''

import task
from dag import DirectedAcyclicGraph
from collections import defaultdict
from heapq import heappush, heappop, heapify, nsmallest
from sys import maxsize
from copy import deepcopy
import json

class TaskOptimizer(object):

    def __init__(self, tasks, dependencies=[]):
        ''' Initializes a directed acyclic graph of tasks in order to
        run optimization methods on it.
        '''
        self.__dag = DirectedAcyclicGraph(tasks, dependencies)
        self.__inv_dag = self.__dag.invertGraph()
        self.__opt_task = defaultdict(tuple)
        self.__task_list = tasks
        for t in tasks:
            self.__opt_task[t] = [0, t.time]


    @classmethod
    def fromGraphDict(cls, dict):
        vertices = []
        edges = []
        for k, v in dict.items():
            vertices.append(k)
            for n in v:
                edges.append((k,n))
        return cls(vertices, edges)


    def tasks(self):
        ''' returns the task list '''
        return self.__task_list


    def addTask(self, task):
        ''' If task is not in task_list, add it to the necessary datastructures
        '''
        if task not in self.__task_list:
            self.__opt_task[task] = [0, task.time]
            self.__task_list.append(task)
            self.__dag.addVertex(task)
            self.__inv_dag.addVertex(task)


    def addDependency(self, dependency):
        ''' Adds a dependency(edge) (of tuple type) to the scheduler
        '''
        (k, v) = tuple(dependency)
        if k not in self.__task_list:
            self.addTask(k)

        if v not in self.__task_list:
            self.addTask(v)

        self.__dag.addEdge(dependency)
        self.__inv_dag.addEdge((v,k))


    def neighbors(self, task):
        ''' Gets all dependent tasks of a designated task (neighbors) '''
        return self.__dag.graph()[task]


    def __reachable(self, task, visited):
        ''' Find all reachable vertices from a source '''
        for n in self.neighbors(task):
            if n not in visited:
                visited.append(n)
                r = self.__reachable(n, visited)
        return visited


    @staticmethod
    def timesort(l, time_dict):
        ''' Sort a list of tasks. Those with higher time value comes first '''
        sorted_l = []
        while l:
            max_val = None
            max_time = 0
            for t in l:
                if time_dict[t] > max_time:
                    max_val = t
                    max_time = time_dict[t]
            sorted_l.append(max_val)
            l.remove(max_val)
        return sorted_l


    @staticmethod
    def containsIndep(l):
        ''' Checks if a list of tasks contains an independent task '''
        for t in l:
            if t.independent:
                return True
        return False


    def optimize(self):
        ''' Optimizes the current sequence of tasks to minimize finish using
        dependencies specified in the DAG. '''
        priority_heap = []
        times_dict = defaultdict(int)
        accumulation_dict = defaultdict(int)
        # Initialize heap with task list / Initialize a dictionary of task times
        for t in self.__task_list:
            heappush(priority_heap, t)
            times_dict[t] = t.time
            accumulation_dict[t] = t.time
        # Topologically sort the tasks
        topolist = self.__dag.toposort()
        # Increment priority of a task for every task that has to come before it
        for t in topolist:
            r = self.__reachable(t, [])
            for v in r:
                v.priority += 1
        # Increment accumulation score* (score of a task based on how long it
        # takes to finish the subsequent tasks after this task), looping in
        # reverse topological order.
        for t in topolist[::-1]:
            r = self.neighbors(t)
            for v in r:
                accumulation_dict[t] += accumulation_dict[v]
        # Heapify the priority queue according to changed priorities
        heapify(priority_heap)

        timestamp = 0             # a timestamp serving as indicator
        finished_tasks = []       # tasks already scheduled
        temp_indep_tasks = []     # list of indep tasks yet to be scheduled
        curr_tasks = []           # tasks prepared to be scheduled
        flag1 = 0                 # flag that helps terminate the while loop
        while priority_heap:
            curr_finished = []    # temporary array for tasks totally done
            curr_adding = []      # temporary array for indep tasks being added

            top_task = heappop(priority_heap)

            # Run while loop to get all tasks that could start simultaneouly
            while top_task.priority == 1:
                if top_task.independent and self.containsIndep(curr_tasks):
                    curr_indep = next(x for x in curr_tasks if x.independent)
                    # Schedule indep task with highest accumulation score* first
                    if accumulation_dict[curr_indep] < \
                       accumulation_dict[top_task]:
                        curr_tasks.remove(curr_indep)
                        finished_tasks.remove(curr_indep)
                        temp_indep_tasks.append(curr_indep)
                        curr_tasks.append(top_task)
                        finished_tasks.append(top_task)
                    else:
                        temp_indep_tasks.append(top_task)
                # Schedule tasks that are not independent
                else:
                    curr_tasks.append(top_task)
                    finished_tasks.append(top_task)
                if priority_heap:
                    top_task = heappop(priority_heap)
                # Break out of while loop if there are top_task priority is 1
                # and there are no more tasks in the heap
                else:
                    flag1 = 1
                    break

            # Top_task at this point isn't priority 1, so add back to heap
            heappush(priority_heap, top_task)

            # Sort tasks based on accumulation score*
            curr_tasks = self.timesort(curr_tasks, accumulation_dict)

            # Schedule all tasks in curr_tasks
            for task in curr_tasks:
                self.__opt_task[task] = \
                    [x + timestamp for x in self.__opt_task[task]]

            # Empty curr_tasks
            curr_tasks = []

            for task in finished_tasks:
                # Decrement remaining time for task by 1 for each iteration
                times_dict[task] -= 1
                # Actions when a task is finished (remaining time is 0)
                if times_dict[task] <= 0:
                    r = self.__reachable(task, [])
                    # Decrease priority of reachable tasks by 1
                    for v in r:
                        v.priority -= 1
                    # If finishing task is independent, prepare to schedule
                    # another independent task
                    if task.independent and temp_indep_tasks:
                        temp_indep_tasks = self.timesort(temp_indep_tasks, \
                                                         accumulation_dict)
                        new_task = temp_indep_tasks.pop(0)
                        curr_tasks.append(new_task)
                        curr_adding.append(new_task)
                    curr_finished.append(task)

            # Modify finished_tasks accordingly
            for task in curr_finished:
                finished_tasks.remove(task)
            for task in curr_adding:
                finished_tasks.append(task)

            # Re-heapify the heap to account for the priority changes
            heapify(priority_heap)
            # Increment timestamp
            timestamp += 1

            # Break out of while loop and terminate if conditions satisfy
            if flag1 and not temp_indep_tasks:
                break


    def getTimestamp(self, task):
        ''' Get optimized timestamp for each task '''
        return self.__opt_task[task]


    def jsonify(self, filename):
        ''' Output a JSON formatted file of the optimized schedule '''
        json_list = []
        for k, v in self.__opt_task.items():
            json_object = {}
            json_object["name"] = k.name
            json_object["description"] = k.description
            json_object["duration"] = k.time
            json_object["timestamp"] = v
            json_list.append(json_object)
        with open(filename, 'w') as fp:
            json.dump(json_list, fp)
        return json_list


    def totalTime(self):
        ''' returns total time it takes to finish all tasks '''
        start_time = maxsize
        end_time = 0
        for k, v in self.__opt_task.items():
            if v[0] < start_time:
                start_time = v[0]
            if v[1] > end_time:
                end_time = v[1]
        return end_time - start_time


    def scheduleGenerator(self):
        ''' A generator that yields a list of the tasks that must be done
        currently.
        '''
        timestamp = 0
        times_dict = defaultdict(int)
        for t in self.__task_list:
            times_dict[t] = t.time
        schedule = deepcopy(self.__opt_task)
        results = []
        while schedule or results:
            curr_del = []
            for k, v in schedule.items():
                if (v[0] <= timestamp) and (v[1] >= timestamp):
                    results.append(k)
                    curr_del.append(k)
            for d in curr_del:
                del schedule[d]
            yield results
            timestamp += 1
            for t in results:
                times_dict[t] -= 1
                if times_dict[t] <= 0:
                    results.remove(t)


    def sortedPrint(self):
        ''' Prints output of schedule sorted by start time '''
        schedule = deepcopy(self.__opt_task)
        while schedule:
            min_task = None
            min_task_timestamp = None
            min_start_time = maxsize
            for k, v in schedule.items():
                if v[0] < min_start_time:
                    min_task = k
                    min_start_time = v[0]
                    min_task_timestamp = v
            del schedule[min_task]
            print(min_task.name + ': [' + str(min_task_timestamp[0]) + \
                  ' ~ ' + str(min_task_timestamp[1]) + ']')

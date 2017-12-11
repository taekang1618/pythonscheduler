''' A Python Class for a scheduling tasks.
Tasks are represented in a directed acyclic graph.
Implements a custom scheduling algorithm using topological sort and priority
queues to optimize the amount of time it takes to finish all tasks.
'''

import task
from dag import DirectedAcyclicGraph
from collections import defaultdict
from heapq import heappush, heappop, heapify, nsmallest
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


    # def __str__(self):
    #     ''' Outputs stringified version of graph dictionary '''
    #     s = "{"
    #     if not self.__vertexSet:
    #         s += "}"
    #     else:
    #         for k, neighbors in self.__graph_dict.items():
    #             s += str(k) + ": ["
    #             if not neighbors:
    #                 s += "], \n "
    #             else:
    #                 for n in neighbors:
    #                     s += str(n) + ","
    #                 s = s[:-1] + "], \n "
    #         s = s[:-4] + "}"
    #     return s


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


    def __reachable(self, task, visited):
        ''' Find all reachable vertices from a source '''
        for n in self.__dag.graph()[task]:
            if n not in visited:
                visited.append(n)
                r = self.__reachable(n, visited)
        return visited


    def optimize(self):
        ''' Optimizes the current sequence of tasks to minimize finish using
        dependencies specified in the DAG. '''
        # depth = defaultdict(int)
        priority_heap = []
        # Set default values for depth stack and inv_depth stack
        for t in self.__task_list:
            heappush(priority_heap, t)
        # Topologically sort the tasks
        topolist = self.__dag.toposort()
        # Increment priority of a task for every task that has to come before it
        for t in topolist:
            r = self.__reachable(t, [])
            for v in r:
                v.priority += 1
        heapify(priority_heap)
        # Maintain a timestamp that will indicate when a task starts/finishes
        timestamp = 0
        curr_priority = 0
        finished_tasks = []
        flag = 0
        while priority_heap:
            curr_tasks = []
            top_task = heappop(priority_heap)
            while top_task.priority == 1:
                curr_tasks.append(top_task)
                finished_tasks.append(top_task)
                if priority_heap:
                    top_task = heappop(priority_heap)
                else:
                    flag = 1
                    break
            heappush(priority_heap, top_task)
            for task in curr_tasks:
                self.__opt_task[task] = \
                    [x + timestamp for x in self.__opt_task[task]]
            for task in finished_tasks:
                task.time -= 1
                if task.time == 0:
                    r = self.__reachable(task, [])
                    for v in r:
                        v.priority -= 1
                    finished_tasks.remove(task)
            heapify(priority_heap)
            timestamp += 1
            if flag:
                break


    def getTimestamp(self, task):
        ''' Get optimized timestamp for each task '''
        return self.__opt_task[task]


    def jsonify(self):
        ''' Output a JSON formatted file of the optimized schedule '''
        string_dict = defaultdict(list)
        for k, v in self.__opt_task.items():
            string_dict[k.name] = v
        with open('result.json', 'w') as fp:
            json.dump(string_dict, fp)
        return string_dict


    def total_time(self):
        

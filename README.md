# pythonscheduler

Teammates : Hye Jin Lee(hyele), Tae Wook Kang(taekan)


# How to use the scheduler
1. Initialize(TaskOptimizer) - There are two ways to initialize the scheduler. The user can either feed in a list of tasks(vertices) and its dependencies(list of edges) or feed in a dictionary formatted graph with tasks and nodes.

ex) { 'A' : ['B', 'C'],
      'B' : ['C', 'E'],            A --> B --> E
      'C' : ['D'],           ==     \   /      |
      'D' : []                       V V       V
      'E' : ['D'] }                   C  ----> D

2. Optimize - Run the optimize() method to assign timestamps for each of the tasks. The output format is a dictionary with Tasks as keys and timestamps as values.

ex) { taskA : [0, 10],
      taskB : [10, 15],
      taskC : [15, 45],
      taskD : [45, 65],
      taskE : [15, 30] }

3. JSONify - After optimizing, the user can run jsonify('filename') to import the optimized schedule dictionary.

4. Generator - After optimizing, the user can run scheduleGenerator() to get a generator that outputs a list of tasks currently being done at each timestep(iteration).

5. Other methods - getTimestamp(task), sortedPrint(), addTask(task), addDependency(dependency)


# Scheduler Classes
1. Task - The task class is an object with an id, name, time it takes to get the task done, description, priority, and a flag that tells if the task should be executed independently from all other tasks.
  * Requirements : 
    1 - descriptor(@total_ordering) and magic methods(__lt__, __eq__) to order tasks based on priority; 
    2 - magic method(__hash__) to enable Task object to be keys
    3 - magic method(__str__) to print task name

2. DirectedAcyclicGraph - This is a generic directed acyclic graph(dag) using a DFS-like method to detect cycles before initializing the graph or adding edges to the graph. There are also useful methods like toposort (topologically sort the dag vertices) and invertGraph (invert the edges in the graph).
  * Requirements :
    1 - uses defaultdict from the collections module

3. TaskOptimizer - This is the main part of our project. This class takes in a list of tasks and dependencies (i.e. a graph with Task objects as nodes) to build an optimized schedule that minimizes the total time it takes to execute all tasks. We use a self-developed optimization algorithm using topological sort, DFS, and several datastructures(heaps, dictionaries, etc.). 
  * Requirements :
    1 - uses a descriptor(@classmethod) to define multiple ways to initialize a Scheduler object
    2 - uses a descriptor(@staticmethod) to write helper functions
    3 - uses a heap from the module heapq to maintain tasks in priority order when running optimize
    4 - other modules (sys.maxsize, copy.deepcopy, json) are used throughout the code
    5 - has a generator method : scheduleGenerator()


# How to use the web app

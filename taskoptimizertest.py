import unittest
from dag import DirectedAcyclicGraph
from task import Task
from taskoptimizer import TaskOptimizer


class TestDAG(unittest.TestCase):

    def setUp(self):
        pass

    # Task
    def test_rational(self):
        task1 = Task('A', 10)
        task2 = Task('B', 5)
        task3 = Task('C', 30)
        task4 = Task('D', 20)
        task5 = Task('E', 15)
        vertices = [task1, task2, task3, task4, task5]
        edgeSet = [(task1, task2), (task1, task3), (task2, task3), (task2, task5),
                 (task3, task4), (task5, task4)]
        edges = [(task1, task2), (task1, task3), (task2, task3), (task2, task5),
                 (task3, task4), (task5, task4)]
        # Test task optimizer init
        opt1 = TaskOptimizer(vertices, edges)
        opt1.optimize()
        self.assertEqual(opt1.getTimestamp(task1), [0,10])
        self.assertEqual(opt1.getTimestamp(task2), [10,15])
        self.assertEqual(opt1.getTimestamp(task3), [15,45])
        self.assertEqual(opt1.getTimestamp(task4), [45,65])
        self.assertEqual(opt1.getTimestamp(task5), [15,30])
        opt1.jsonify()




def main():
    unittest.main()

if __name__ == '__main__':
    main()

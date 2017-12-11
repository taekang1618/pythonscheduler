import unittest
from dag import *
from task import *


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
        # Test graph init
        dag1 = DirectedAcyclicGraph(vertices)
        dag2 = DirectedAcyclicGraph(vertices, edges)
        print(str(dag1))
        print(str(dag2))
        self.assertEqual(dag2.edges(), edgeSet)
        # Test add edge (cycle detection)
        dag2.addEdge((task4, task5))
        dag2.addEdge((task4, task1))
        self.assertEqual(dag2.edges(), edgeSet)
        task6 = Task('F', 0)
        print(len(dag2.edges()))
        dag2.addVertex(task6)
        dag2.addEdge((task1, task6))
        edgeSet.append((task1, task6))
        vertices.append(task6)
        self.assertEqual(dag2.edges(), edges)
        self.assertEqual(dag2.vertices(), vertices)
        # Test toposort
        t_result = dag2.toposort()
        for v in t_result:
            print(v.name)
        # Test invert
        inv_dag2 = dag2.invertGraph()
        print(str(dag2))
        print(str(inv_dag2))



def main():
    unittest.main()

if __name__ == '__main__':
    main()

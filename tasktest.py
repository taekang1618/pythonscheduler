import unittest
from task import *
from heapq import heappush, heappop, heapify


class TestTask(unittest.TestCase):

    def setUp(self):
        pass

    # Task
    def test_rational(self):
        task1 = Task('A', 10)
        task2 = Task('B', 5)
        task3 = Task('C', 30)
        task4 = Task('D', 20)
        task5 = Task('E', 15)
        # task1.addChildren([task2, task3])
        # self.assertEqual(task1.children, [task2, task3])
        # print("Throw self edge error message: ")
        # task1.addChild(task1)
        # print("Throw child already exists error message: ")
        # task1.addChild(task2)
        # self.assertEqual(task1.children, [task2, task3])
        # task2.addChild(task3)
        # task2.addChild(task5)
        # task2.addParent(task1)
        # task3.addChild(task4)
        # task3.addParents([task1, task2])
        # task4.addParent(task3)
        # task4.addParent(task5)
        # task5.addChild(task4)
        # task1.removeChild('B')
        # self.assertEqual(task1.children, [task3])
        heap = []
        task1.editPriority(5)
        task2.editPriority(6)
        task3.editPriority(3)
        task4.editPriority(4)
        heappush(heap, task1)
        heappush(heap, task2)
        heappush(heap, task3)
        heappush(heap, task4)
        task4.editPriority(2)
        heapify(heap)
        print(heappop(heap).name)
        print(heappop(heap).name)
        print(heappop(heap).name)
        print(heappop(heap).name)


def main():
    unittest.main()

if __name__ == '__main__':
    main()

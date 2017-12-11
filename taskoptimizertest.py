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
        # Dictionary version of graph
        graph_dict = {task1: [task2, task3],
                task2: [task3, task5],
                task3: [task4],
                task4: [],
                task5: [task4]}
        vertices = [task1, task2, task3, task4, task5]
        time_dict = {task1: 80,
                     task2: 70,
                     task3: 50,
                     task4: 20,
                     task5: 45}
        l = TaskOptimizer.timesort(vertices, time_dict)
        self.assertEqual(l, [task1, task2, task3, task5, task4])
        vertices = [task1, task2, task3, task4, task5]
        edgeSet = [(task1, task2), (task1, task3), (task2, task3), (task2, task5),
                 (task3, task4), (task5, task4)]
        edges = [(task1, task2), (task1, task3), (task2, task3), (task2, task5),
                 (task3, task4), (task5, task4)]
        # Test task optimizer init
        opt1 = TaskOptimizer(vertices, edges)
        opt1.optimize()
        # Task optimizer created with a dictionary
        opt2 = TaskOptimizer.fromGraphDict(graph_dict)
        opt2.optimize()
        self.assertEqual(opt1.getTimestamp(task1), [0,10])
        self.assertEqual(opt1.getTimestamp(task2), [10,15])
        self.assertEqual(opt1.getTimestamp(task3), [15,45])
        self.assertEqual(opt1.getTimestamp(task4), [45,65])
        self.assertEqual(opt1.getTimestamp(task5), [15,30])
        # Dictionary version tests
        self.assertEqual(opt2.getTimestamp(task1), [0,10])
        self.assertEqual(opt2.getTimestamp(task2), [10,15])
        self.assertEqual(opt2.getTimestamp(task3), [15,45])
        self.assertEqual(opt2.getTimestamp(task4), [45,65])
        self.assertEqual(opt2.getTimestamp(task5), [15,30])
        # opt1.jsonify() # Creates a JSON file of the optimized schedule output
        self.assertEqual(opt1.totalTime(), 65)
        gen = opt1.scheduleGenerator()
        for i in range(60):
            print('Timestamp: ' + str(i))
            for t in next(gen):
                print(t.name)

        # A different graph (Gordon Ramsey's Perfect Burger Tutorial)
        # Link : https://www.youtube.com/watch?v=iM_KMYulI_s
        T1 = Task('Season the Patties', 45, "Use salt, pepper, and grape " + \
                   "seed oil (or vegetable oil) to season the beef patty. " + \
                   "Leave the meat to rest and don't let the meat be cold. ", True)
        T2 = Task('Heat up the Frying Pan', 100, "Heat up the pan (or grill) " + \
                   "piping hot.")
        T3 = Task('Cook the meat', 360, "Let the meat sear in the pan. Flip it " + \
                   "twice and no more.")

        T4 = Task('Cook the bun', 240, "There is nothing worse than a soggy " + \
                   "bun. Flip the bun once.")

        T5 = Task('Cut the onions', 40, "Peel the onions and cut them in " + \
                   "nice circular shape.", True)
        T6 = Task('Season the onions', 20, "Use salt and pepper on the " +\
                   "onions.", True)
        T7 = Task('Cook the onions', 300, "Caramelize the onion on the pan.")

        T8 = Task('Wash the lettuce', 30, "Cleanse the lettuce with " + \
                   "water.", True)
        T9 = Task('Place the lettuce', 5, "Break the lettuce in half and " + \
                   "place it on the burger in good shape.", True)

        T10 = Task('Cut the tomato', 40, "Cut the tomato in circular " + \
                    "shapes.", True)
        T11 = Task('Place the tomato', 15, "Place the tomato on the bun and " + \
                    "add a little bit of salt & pepper.", True)

        T12 = Task('Make honey-mustard & mayo sauce', 60, "Mix mayonnaise " + \
                    "and honey mustard for a tasty burger sauce.", True)
        T13 = Task('Spread sauce on bread', 10, "Spread the sauce on both " + \
                    "sides of the bun.", True)
        T14 = Task('Brush butter on the patties', 20, "With a brush, touch " + \
                    "the patties gently with a little bit of butter.", True)
        T15 = Task('Put cheddar cheese on the patties', 60, "Place cheddar " + \
                    "cheese on the cooking patties and rest until it melts.")
        T16 = Task('Place patty on the burger', 20, "With care, place the " + \
                    "cooked patty on the burger.", True)
        T17 = Task('Place the onion on the burger', 20, "With care, place " + \
                    "the caramelized onion on top of the patty.", True)
        T18 = Task('Close the top bun and serve', 30, "Close the top bun of " + \
                    "the burger and place the burger on a dish to serve.", True)

        burger_graph = {T1: [T3],
                        T2: [T3, T4, T7],
                        T3: [T16],
                        T4: [T11, T13],
                        T5: [T6],
                        T6: [T7],
                        T7: [T17],
                        T8: [T9],
                        T9: [T11],
                        T10: [T11],
                        T11: [T16],
                        T12: [T13],
                        T13: [T9, T14],
                        T14: [T15],
                        T15: [T16],
                        T16: [T17],
                        T17: [T18],
                        T18: []
                        }
        burger_optimizer = TaskOptimizer.fromGraphDict(burger_graph)
        burger_optimizer.optimize()
        burger_optimizer.sortedPrint()
        burger_optimizer.jsonify('burger.json')



def main():
    unittest.main()

if __name__ == '__main__':
    main()

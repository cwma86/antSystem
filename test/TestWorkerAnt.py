#!/usr/bin/env python3
import logging
import os
import sys
import unittest

script_path = os.path.dirname(os.path.abspath( __file__ ))
src_dir = os.path.join(script_path, "../src")
sys.path.insert(1, src_dir)
from Environment import Environment
from WorkerAnt import WorkerAnt

logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s\
                [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.DEBUG)

class TestWorkerAnt(unittest.TestCase):
  def test_invalidInputFile(self):
    foodSources = [ (1, 1.0, 1.0), 
                    (2, 1.0, 2.0),
                    (3, 1.0, 3.0),
                    (4, 1.0, 4.0),
                    (5, 1.0, 5.0),
]
    environment = Environment(foodSources, workerAntCount=2)
    workerAnts = []
    workerAnt = WorkerAnt(environment)
    # Hack to remove the randomness out of WorkerAnt's constructor
    startingSpot = environment.FoodSources[0]
    workerAnt.CurrentFoodSource = startingSpot
    workerAnt.VisitedFoodSources = [startingSpot]
    workerAnt.Environment = environment
    workerAnts.append(workerAnt)
    workerAnt = WorkerAnt(environment)
    # Hack to remove the randomness out of WorkerAnt's constructor
    startingSpot = environment.FoodSources[3]
    workerAnt.CurrentFoodSource = startingSpot
    workerAnt.VisitedFoodSources = [startingSpot]
    workerAnt.Environment = environment
    workerAnts.append(workerAnt)

    pheromoneTrails = environment._Environment__runWorkerAnts(workerAnts)

    self.assertEqual(len(pheromoneTrails), 5)
    sortedTrails = list(sorted(pheromoneTrails.items(), key=lambda item: item[1], reverse=True))
    key, value = sortedTrails[0]
    self.assertEqual(key, ((1, 1.0, 1.0), (2, 1.0, 2.0)))
    self.assertEqual(value, 2)
    key, value = sortedTrails[1]
    self.assertEqual(key, ((2, 1.0, 2.0), (3, 1.0, 3.0)))
    self.assertEqual(value, 2)
    key, value = sortedTrails[2]
    self.assertEqual(key, ((3, 1.0, 3.0), (4, 1.0, 4.0)))
    self.assertEqual(value, 2)
    key, value = sortedTrails[3]
    self.assertEqual(key, ((4, 1.0, 4.0), (5, 1.0, 5.0)))
    self.assertEqual(value, 1)
    key, value = sortedTrails[4]
    self.assertEqual(key, ((1, 1.0, 1.0), (5, 1.0, 5.0)))
    self.assertEqual(value, 1)


if __name__ == '__main__':
    unittest.main()
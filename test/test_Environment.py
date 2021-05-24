#!/usr/bin/env python3
import logging
import os
import sys
import unittest

script_path = os.path.dirname(os.path.abspath( __file__ ))
src_dir = os.path.join(script_path, "..","src")
sys.path.insert(1, src_dir)
from Environment import Environment
from FoodSource import FoodSource

logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s\
                [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)

class test_Environment(unittest.TestCase):
  def test_validInputFile(self):
    foodSources = [ FoodSource("1 1.0 1.0"), 
                    FoodSource("2 1.0 2.0"),
                    FoodSource("3 1.0 3.0"),
                    FoodSource("4 1.0 4.0"),
                    FoodSource("5 1.0 5.0"),
                    FoodSource("6 2.0 1.0"),
                    FoodSource("7 3.0 1.0"),
                    FoodSource("8 4.0 1.0"),
                    FoodSource("9 5.0 1.0"),
                    FoodSource("10 10.0 10.0")]
    environment = Environment(foodSources, workerAntCount=1)
    pheromoneTrails = environment.explore()
    sortedTrails = dict(sorted(pheromoneTrails.items(), key=lambda item: item[1], reverse=True))
    logging.debug(sortedTrails)
    self.assertEqual(len(sortedTrails), 9)


if __name__ == '__main__':
    unittest.main()
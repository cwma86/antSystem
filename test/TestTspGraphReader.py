#!/usr/bin/env python3
import logging
import os
import sys
import unittest

script_path = os.path.dirname(os.path.abspath( __file__ ))
src_dir = os.path.join(script_path, "../src")
sys.path.insert(1, src_dir)
from TspGraphReader import TspGraphReader

logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s\
                [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)

class TestTspGraphReader(unittest.TestCase):
  def test_invalidInputFile(self):
    testFilename = "aksdf"
    tspGraph = TspGraphReader(filename=testFilename)
    self.assertEqual(tspGraph, None)

  def test_validInputFile(self):
    testFilename = os.path.join(script_path, '../TSPData/pla85900.tsp')
    tspGraph = TspGraphReader(filename=testFilename)
    self.assertNotEqual(tspGraph, None)

  def test_validHeaderParse(self):
    testFilename = os.path.join(script_path, '../TSPData/pla85900.tsp')
    tspGraph = TspGraphReader(filename=testFilename)
    self.assertEqual(tspGraph.graphName, "pla85900")
    self.assertEqual(tspGraph.graphComment, "Programmed logic array (Johnson)")
    self.assertEqual(tspGraph.graphType, "TSP")
    self.assertEqual(tspGraph.edgeType, "CEIL_2D")
    self.assertEqual(tspGraph.dimension, 85900)

  def test_validDataParse(self):
    testFilename = os.path.join(script_path, '../TSPData/pla85900.tsp')
    tspGraph = TspGraphReader(filename=testFilename)
    # Check length
    self.assertEqual(len(tspGraph.foodSources), 85900)

    # Check first row
    self.assertEqual(tspGraph.foodSources[0][0], 1)
    self.assertAlmostEqual(tspGraph.foodSources[0][1], 1449000.0)
    self.assertAlmostEqual(tspGraph.foodSources[0][2], 672250.0)

    # Check middle row
    self.assertEqual(tspGraph.foodSources[42513][0], 42514)
    self.assertAlmostEqual(tspGraph.foodSources[42513][1], 867250.0)
    self.assertAlmostEqual(tspGraph.foodSources[42513][2], 965300.0)

    # Check last row
    self.assertEqual(tspGraph.foodSources[85899][0], 85900)
    self.assertAlmostEqual(tspGraph.foodSources[85899][1], 1339150.0)
    self.assertAlmostEqual(tspGraph.foodSources[85899][2], 682900.0)

if __name__ == '__main__':

    unittest.main()
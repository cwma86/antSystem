#!/usr/bin/env python3
import logging
import os
import sys
import unittest

script_path = os.path.dirname(os.path.abspath( __file__ ))
src_dir = os.path.join(script_path, "../src")
sys.path.insert(1, src_dir)
from TspGraph import TspGraph

logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s\
                [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)

class TestTspGraph(unittest.TestCase):
  def test_invalidInputFile(self):
    testFilename = "aksdf"
    tspGraph = TspGraph(filename=testFilename)
    self.assertEqual(tspGraph, None)

  def test_validInputFile(self):
    testFilename = os.path.join(script_path, '../TSPData/pcb10_test.tsp')
    tspGraph = TspGraph(filename=testFilename)
    self.assertNotEqual(tspGraph, None)

  def test_validHeaderParse(self):
    testFilename = os.path.join(script_path, '../TSPData/pcb10_test.tsp')
    tspGraph = TspGraph(filename=testFilename)
    self.assertEqual(tspGraph.graphName, "pcb10")
    self.assertEqual(tspGraph.graphComment, "Drilling problem (Juenger/Reinelt)")
    self.assertEqual(tspGraph.graphType, "TSP")
    self.assertEqual(tspGraph.edgeType, "EUC_2D")
    self.assertEqual(tspGraph.dimension, 10)

  def test_validDataParse(self):
    testFilename = os.path.join(script_path, '../TSPData/pcb10_test.tsp')
    tspGraph = TspGraph(filename=testFilename)
    # Check length
    self.assertEqual(len(tspGraph.foodSources), 10)

    # Check first row
    self.assertEqual(tspGraph.foodSources[0][0], 1)
    self.assertAlmostEqual(tspGraph.foodSources[0][1], 2.01700e+03)
    self.assertAlmostEqual(tspGraph.foodSources[0][2], 6.63000e+02)

    # Check middle row
    self.assertEqual(tspGraph.foodSources[4][0], 5)
    self.assertAlmostEqual(tspGraph.foodSources[4][1],  2.01600e+03)
    self.assertAlmostEqual(tspGraph.foodSources[4][2], 8.17000e+02)

    # Check last row
    self.assertEqual(tspGraph.foodSources[9][0], 10)
    self.assertAlmostEqual(tspGraph.foodSources[9][1], 1.96300e+03)
    self.assertAlmostEqual(tspGraph.foodSources[9][2], 8.77000e+02)

if __name__ == '__main__':
    unittest.main()
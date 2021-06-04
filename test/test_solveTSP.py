#!/usr/bin/env python3
import argparse
import datetime
import logging
import math
import os
import sys
import unittest


script_path = os.path.dirname(os.path.abspath( __file__ ))
Runner_dir = os.path.join(script_path, "..", "src", "Runner")
sys.path.insert(1, Runner_dir)
from solveTSP import solveTSP

logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s\
                [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)

dataPath = os.path.join(script_path, '..', 'TSPData')

class Arg:
  def __init__(self):
    self.filename = ""
    self.workerAntCount = 0
    self.Brute = False
    self.AntSystem = True
    self.MCTS = False
    self.MMAS = False

class test_solveTSP(unittest.TestCase):
  def test_solveTSP(self):
    args = Arg()
    filePath = os.path.join(dataPath,'pcb10_test.tsp')
    args.filename = filePath
    args.Brute = True
    args.AntSystem = False
    args.MCTS = False
    args.MMAS = False
    failCount = 0 
    numberOfRuns = 1
    now = datetime.datetime.now()
    for i in range(numberOfRuns):
      bestSolution, bestDist, tspData = solveTSP(args)
      if not math.isclose(bestDist, 638.108, abs_tol=0.001):
        failCount +=1
        logging.info(f"Incorrect path bestDist: {bestDist:.2f}")
    avgCorrect = (numberOfRuns-failCount)/numberOfRuns*100
    print(f"average correct solution {avgCorrect:.2f}%")
    self.assertAlmostEqual(avgCorrect, 100.0)


  def test_solveTSPAnt(self):
    args = Arg()
    filePath = os.path.join(dataPath,'lin12.tsp')
    args.filename = filePath
    args.Brute = False
    args.AntSystem = True
    args.MCTS = False
    args.MMAS = False
    failCount = 0 
    numberOfRuns = 30
    initTime = datetime.datetime.now()
    for i in range(numberOfRuns):
      bestSolution, bestDist, tspData = solveTSP(args)
      if not math.isclose(bestDist, 2825.271, abs_tol=0.001):
        failCount +=1
        logging.info(f"Incorrect path bestDist: {bestDist:.2f}")
    finalTime = datetime.datetime.now()
    timeDelta = finalTime - initTime
    avgRunTime = timeDelta / numberOfRuns
    avgCorrect = (numberOfRuns-failCount)/numberOfRuns*100
    logging.info(f"average AS time per run {avgRunTime.total_seconds():.3f} seconds")
    logging.info(f"average AS correct solution {avgCorrect:.2f}%")
    self.assertGreaterEqual(avgCorrect, 70)

  def test_solveTSPMMAnt(self):
    args = Arg()
    filePath = os.path.join(dataPath,'lin12.tsp')
    args.filename = filePath
    args.Brute = False
    args.AntSystem = False
    args.MCTS = False
    args.MMAS = True
    failCount = 0 
    numberOfRuns = 30
    initTime = datetime.datetime.now()
    for i in range(numberOfRuns):
      bestSolution, bestDist, tspData = solveTSP(args)
      if not math.isclose(bestDist, 2825.271, abs_tol=0.001):
        failCount +=1
        logging.info(f"Incorrect path bestDist: {bestDist:.2f}")
    finalTime = datetime.datetime.now()
    timeDelta = finalTime - initTime
    avgRunTime = timeDelta/ numberOfRuns
    avgCorrect = (numberOfRuns-failCount)/numberOfRuns*100
    logging.info(f"average MMAS time per run {avgRunTime.total_seconds():.3f} seconds")
    logging.info(f"average MMAS correct solution {avgCorrect:.2f}%")
    self.assertGreaterEqual(avgCorrect, 80)






if __name__ == '__main__':
    unittest.main()
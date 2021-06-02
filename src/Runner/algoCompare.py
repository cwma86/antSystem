#!/usr/bin/env python3
import argparse
import logging
import math
import os
import sys
import cv2 as cv
import numpy as np
import time

from ImageCreator import createImage

script_path = os.path.dirname(os.path.abspath( __file__ ))
# Generic TSP support imports
support_dir = os.path.join(script_path, "..","Support")
sys.path.insert(1, support_dir)
from SymetricMatrix import SymetricMatrix
from TspParser import TspParser

# AntSystem imports
AntSystem_dir = os.path.join(script_path, "..","AntSystem")
sys.path.insert(1, AntSystem_dir)
from AntSystem import AntSystem

# Min Max AntSystem imports
AntSystem_dir = os.path.join(script_path, "..","MMAntSystem")
sys.path.insert(1, AntSystem_dir)
from MMAntSystem import MMAntSystem

# MSTS AntSystem imports
MCTS_dir = os.path.join(script_path, "..","MCTS")
sys.path.insert(1, MCTS_dir)
from MonteCarloAntColony import MonteCarloAntColony

# Brute Force imports
Brute_dir = os.path.join(script_path, "..","BruteForce")
sys.path.insert(1, Brute_dir)
from BruteForce import brute_force_solution

# Brute Force imports
Brute_dir = os.path.join(script_path, "..")
sys.path.insert(1, Brute_dir)
from TspGraph import TspGraph

def args():
  defaultFilePath = os.path.join(script_path, '..', '..', 'TSPData','pcb10_test.tsp')
  parser = argparse.ArgumentParser(description='Run Ant System')   
  parser.add_argument('--filename', default=defaultFilePath, type=str,
                      help='file path of tsp data')
  parser.add_argument('--noBrute', action='store_true',
                      help='Do not use brute force or calculate ')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='verbose logging')
  args = parser.parse_args()

  # initialize logger format
  logLevel = logging.INFO
  if args.verbose:
    logLevel = logging.DEBUG
  logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s\
       [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logLevel)
  logging.info(f"logging set to {logging.DEBUG}")
  return args

def logOutput(deltaTime, solutionPath, pathDistance, tspData, name):
  print(f"Elapsed Time: {deltaTime:0.2f} milliseconds")
  createImage( solutionPath, tspData, outFile=f"{name}.png")
  print(f"{name} Best Solution:")
  solutionString = "  "
  for i in range(len(solutionPath)):
    solutionString += (f"node[{i}]: {solutionPath[i]-1}, ")
    if i % 5 == 4:
      print(solutionString)
      solutionString = "  "
  if len(solutionString) > 2:
    print(solutionString)
  print(f"{name} bestDist: {pathDistance:0.2f}")


def algoCompare(inputargs):
  # Intake File
  tspData = TspParser(inputargs.filename)
  logging.debug(f"{len(tspData.nodes)} nodes created")
  logging.debug(tspData.data_to_string())

  # Run Brute Force
  bruteDist = 0
  bruteSolution = []
  if not inputargs.noBrute:
    brutestart = time.time()
    bruteSolution, bruteDist = brute_force_solution(tspData)  
    bruteend = time.time()
    bruteDt = (bruteend-brutestart)*1000 # Millisec
    outFile="brute"
    logOutput(bruteDt, bruteSolution, bruteDist, tspData, outFile)


  numberOfRuns = 10
  failCount = 0
  # Run Regular Ant System
  numOfAnts = tspData.dimension
  numAttempts = tspData.dimension * tspData.dimension
  dtSum = 0
  if not inputargs.noBrute: #removing normal AS to save time
    for i in range(numberOfRuns):
      antstart = time.time()
      antSystem = AntSystem(tspData, numOfAnts=numOfAnts, 
                                    numberOfAttempts=numAttempts, 
                                    pheromoneDecay=0.99)
      antSolution = antSystem.bestSolution
      antDist = antSystem.bestDist
      antend = time.time()
      antDt = (antend-antstart)*1000 # Milli Sec
      dtSum += antDt
      if not inputargs.noBrute:
        if not np.isclose(antDist, bruteDist):
          failCount += 1
    avgOptimal = (numAttempts-failCount)/numAttempts
    avgRunTime = dtSum/numAttempts
    name="AS"
    print(f"{name} avgOptimal solution: {avgOptimal*100}%")
    print(f"{name} avgRunTime: {avgRunTime}")
    logOutput(antDt, antSolution, antDist, tspData, name)

  # Run Min-Max Antsystem
  numOfAnts = tspData.dimension
  numAttempts = int( tspData.dimension * math.log(tspData.dimension) )
  failCount = 0
  dtSum = 0
  MMASDist = 0
  minMMASDist = float("inf")
  for i in range(numberOfRuns):
    MMASstart = time.time()
    antSystem = MMAntSystem(tspData, numOfAnts=numOfAnts, 
                                  numberOfAttempts=numAttempts, 
                                  pheromoneDecay=0.98)
    MMASSolution = antSystem.bestSolution
    MMASDist = antSystem.bestDist
    MMASend = time.time()
    MMASDt = (MMASend-MMASstart)*1000
    dtSum += MMASDt
    if not inputargs.noBrute:
      if not np.isclose(MMASDist, bruteDist):
        failCount += 1
    else:
      if MMASDist < minMMASDist:
         minMMASDist = MMASDist
  avgOptimal = (numAttempts-failCount)/numAttempts
  avgRunTime = dtSum/numAttempts
  name="MMAS"
  print(f"{name} avgOptimal solution: {avgOptimal*100}%")
  print(f"{name} avgRunTime: {avgRunTime}")
  logOutput(MMASDt, MMASSolution, MMASDist, tspData, name)

  # Run MCTS
  failCount = 0
  dtSum = 0
  MCTSDist = 0
  tollerance = 1.0
  for i in range(numberOfRuns):
    workerAntCount = 20 # default number of ants
    MCTSstart = time.time()
    tspGraph = TspGraph(filename=inputargs.filename, workerAntCount=workerAntCount)

    # Store Solution
    MCTSSolution = tspGraph.bestTour
    MCTSDist = tspGraph.bestScore

    # Calc Time delta
    MCTSend = time.time()
    MCTSDt = (MCTSend-MCTSstart)*1000
    dtSum += MCTSDt

    # Determine if solution is optimal
    if not inputargs.noBrute:
      if not np.isclose(MMASDist, bruteDist):
        failCount += 1
    else:
      # Consider the lowest solution for MMAS as optimal and compare
      if MCTSDist > (minMMASDist + tollerance):
        failCount += 1
  avgOptimal = (numAttempts-failCount)/numAttempts
  avgRunTime = dtSum/numAttempts
  name="MCTS"
  print(f"{name} avgOptimal solution: {avgOptimal*100}%")
  print(f"{name} avgRunTime: {avgRunTime}")
  logOutput(MCTSDt, MCTSSolution, MCTSDist, tspData, name)


if __name__ == "__main__":
  inputargs = args()
  algoCompare(inputargs)

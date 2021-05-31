#!/usr/bin/env python3
import argparse
import logging
import math
import os
import sys

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

def args():
  defaultFilePath = os.path.join(script_path, '..', '..', 'TSPData','pcb10_test.tsp')
  parser = argparse.ArgumentParser(description='Run Ant System')   
  parser.add_argument('--filename', default=defaultFilePath, type=str,
                      help='file path of tsp data')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='verbose logging')
  parser.add_argument('--MCTS', action='store_true', default=True,
                      help='Run Monte Carlo Tree Search Algorithm (default)')
  parser.add_argument('--AntSystem', action='store_true',
                      help='Run Ant Colony Optimization Algorithm')
  parser.add_argument('--MMAS', action='store_true',
                      help='Run Min-Max Ant Colony Optimization Algorithm')
  parser.add_argument('--Brute', action='store_true',
                      help='Run Brute Force Algorithm')
  parser.add_argument('-a', '--workerAntCount', type=int, 
                      help='The amount of Worker Ants to crawl '
                        + 'the food sources and leave pheromone trails')
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
  if args.Brute:
    logging.info("Running brute force algorithm")
    args.AntSystem = False
    args.MCTS = False
    args.MMAS = False
  elif args.AntSystem:
    logging.info("Running Ant Colony Optimization algorithm")
    args.Brute = False
    args.MCTS = False
    args.MMAS = False
  elif args.MMAS:
    logging.info("Running Min-Max Ant Colony Optimization algorithm")
    args.AntSystem = False
    args.Brute = False
    args.MCTS = False
  else:
    logging.info("Running Monte Carlo Tree Search Ant Colony Optimization algorithm")
    args.AntSystem = False
    args.Brute = False
    args.MMAS = False
 
  return args


def solveTSP(inputargs):
  # Get data from file
  tspData = TspParser(inputargs.filename)
  logging.debug(f"{len(tspData.nodes)} nodes created")
  logging.debug(tspData.data_to_string())
  bestSolution = []
  bestDist = 0
  if inputargs.Brute:
    bestSolution, bestDist = brute_force_solution(tspData)  
  elif inputargs.AntSystem:
    # Algorith Tuning
    numOfAnts = tspData.dimension
    if numOfAnts < 2:
      numOfAnts = 2 
    numAttempts = tspData.dimension * tspData.dimension
    #numAttempts = int(tspData.dimension * 5 * math.log(tspData.dimension) // 1)
    #numAttempts = tspData.dimension
    antSystem = AntSystem(tspData, numOfAnts=numOfAnts, 
                                  numberOfAttempts=numAttempts, 
                                  pheromoneDecay=0.99)
    bestSolution = antSystem.bestSolution
    bestDist = antSystem.bestDist

  elif inputargs.MMAS:
    # Algorith Tuning
    numOfAnts = tspData.dimension
    if numOfAnts < 2:
      numOfAnts = 2 
    #numAttempts = tspData.dimension * tspData.dimension
    numAttempts = int( tspData.dimension * math.log(tspData.dimension) )
    #numAttempts = tspData.dimension
    antSystem = MMAntSystem(tspData, numOfAnts=numOfAnts, 
                                  numberOfAttempts=numAttempts, 
                                  pheromoneDecay=0.98)
    bestSolution = antSystem.bestSolution
    bestDist = antSystem.bestDist
  else:
    logging.info(f"doing MCTS")
    # Algorith Tuning
    numOfAnts = tspData.dimension //2
    if numOfAnts < 2:
      numOfAnts = 2 
    #numAttempts = tspData.dimension * tspData.dimension
    numAttempts = int( tspData.dimension * math.log(tspData.dimension) )
    #numAttempts = tspData.dimension
    antSystem = MonteCarloAntColony(tspData, numOfAnts=numOfAnts, 
                                  numberOfAttempts=numAttempts, 
                                  pheromoneDecay=0.98)
    bestSolution = antSystem.bestSolution
    bestDist = antSystem.bestDist

  logging.debug("pheromone\n" + tspData.pheromone_to_string())
  logging.debug("cost\n" + tspData.cost_to_string())

  return bestSolution, bestDist
  
if __name__ == "__main__":
  inputargs = args()
  bestSolution, bestDist = solveTSP(inputargs)
  print(f"Best Solution:")
  solutionString = "  "
  for i in range(len(bestSolution)):
    solutionString += (f"node[{i}]: {bestSolution[i]}, ")
    if i % 5 == 4:
      print(solutionString)
      solutionString = "  "
  if len(solutionString) > 2:
    print(solutionString)
  print(f"bestDist: {bestDist}")

import logging
import os
import random
import sys

from MonteCarloTSmod import MonteCarloTSmod
from MonteCarloAntColonyNode import MonteCarloAntColonyNode

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, '..', 'Support'))
from SymetricMatrix import SymetricMatrix
from TspData import TspData
from TspData import calculate_path_distance

sys.path.append(os.path.join(file_path, '..', 'AntSystem'))
from AntSystem import AntSystem
from AntSystem import update_best_solution

sys.path.append(os.path.join(file_path, '..', 'MCTS'))

class MonteCarloAntColony(AntSystem):
  def __init__(self, tspData, numOfAnts=2, numberOfAttempts = 20, 
              pheromoneDecay=0.9, beta=2.0, alpha=1.0):
    self.isPheromoneInit = False
    super().__init__(tspData, numOfAnts, numberOfAttempts, 
                     pheromoneDecay, beta, alpha)

  def tour_construct_solution(self, tspData, solution):
    if len(solution) < 1:
      logging.error(f"this should not happen")
      return
    freeNodes = list(tspData.nodes)
    for freeNode1 in freeNodes:
      if freeNode1.nodeId == solution[0]:
        freeNodes.remove(freeNode1)
        break

    MCTS = MonteCarloTSmod(explorParam=1)
    MCTSNode = MonteCarloAntColonyNode(tspData, solution, freeNodes, self.bestSolution)
    simulationsToTrain = 10
    # build greedy MST
    while len(MCTSNode.freeNodesList): # create a solution using all available nodes
      for _ in range(simulationsToTrain):
        MCTS.simulate(MCTSNode)
      MCTSNode = MCTS.selectBestNode(MCTSNode)
    return MCTSNode.solutionList

import logging
import os
import random
import sys

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, '..', 'Support'))
from SymetricMatrix import SymetricMatrix
from TspData import TspData
from TspData import calculate_path_distance
sys.path.append(os.path.join(file_path, '..', 'AntSystem'))
from AntSystem import AntSystem
from AntSystem import update_best_solution

class MMAntSystem(AntSystem):
  def __init__(self, tspData, numOfAnts=2, numberOfAttempts = 20, 
              pheromoneDecay=0.9, beta=2.0, alpha=1.0):
    self.isPheromoneInit = False
    tmax = 3000
    tspData.adjust_max_pheromone(tmax)
    super().__init__(tspData, numOfAnts, numberOfAttempts, 
                     pheromoneDecay, beta, alpha)

  def apply_pheromone(self, tspData, solutions):
    q = 1  # Pheromone constant
    if not self.isPheromoneInit:
      # init pheromone level to max
      tmax = 1/(1-self.decay) * q/self.bestDist
      tspData.adjust_max_pheromone(tmax)
      self.isPheromoneInit = True
    tspData.evaporate_pheromone(self.decay)
    prevNode = None
    currNode = None
    iterBestSolution = None
    iterBestDist = float('inf')
    for solution in solutions:
      distance = calculate_path_distance(solution, tspData)
      if distance < iterBestDist or iterBestSolution == None:
        iterBestDist = distance
        iterBestSolution = solution
      
    # TODO make tuneable
    selectParam = .2
    randVal = random.uniform(0,1)
    bestDist = iterBestDist
    bestSolution = iterBestSolution
    if randVal < selectParam:
      # Update global best instead of iter best
      bestDist = self.bestDist
      bestSolution = self.bestSolution
    for node in bestSolution:
      if prevNode is None:
        prevNode = node
        continue
      currNode = node
      # Update pheromone
      currValue = tspData.get_pheromone(currNode, prevNode)
      currValue += q/bestDist
      tspData.set_pheromone(currNode, prevNode, currValue)
      tmax =  1/(1-self.decay)  * q/self.bestDist

      # limit pheromone to tmax
      tspData.adjust_max_pheromone(tmax)

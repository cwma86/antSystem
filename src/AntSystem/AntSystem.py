import logging
import os
import random
import sys

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, '..', 'Support'))
from TspData import TspData
from TspData import calculate_path_distance

class AntSystem:
  def __init__(self, tspData, numOfAnts=2, numberOfAttempts = 20, 
              pheromoneDecay=0.9, beta=1, alpha=1):
    self.beta = beta # beta for tuning distance weight in cost
    self.alpha = alpha # alpha for tuning pheromone weight in cost
    self.decay = pheromoneDecay 
    inc = 0
    self.bestSolution = None
    self.bestDist = float('inf')
    logging.debug(f"runnging for {numberOfAttempts} attempts")
    while(True):
      solutions = []
      for i in range(numOfAnts):
        # Select a random starting point
        startNode = random.randint(1,tspData.dimension)
        solutions.append([startNode])

      for i in range(numOfAnts):
        solutions[i] = self.tour_construct_solution( tspData, solutions[i])
        solutions[i] = self.local_search(solutions[i])
      self.bestSolution, self.bestDist = update_best_solution(self.bestSolution, 
                                                              self.bestDist, 
                                                              solutions, tspData)
      self.apply_pheromone(tspData, solutions)

      #temp
      if inc > numberOfAttempts:
        break
      if inc % 20 == 0:
        logging.debug(f"attempt: {inc} best distance: {self.bestDist}")

      inc += 1
      

  def tour_construct_solution(self, tspData, solution):
    if len(solution) < 1:
      logging.error(f"this should not happen")
      return
    freeNodes = set(tspData.nodes)
    for freeNode1 in freeNodes:
      if freeNode1.nodeId == solution[0]:
        freeNodes.discard(freeNode1)
        break

    # build greedy MST
    while len(freeNodes): # create a solution using all available nodes
      freeNodestmp = freeNodes.copy()
      maxCost = 0
      nextNode = None
      costSum = 0
      for freenode2 in freeNodestmp:
        # get sum of all possible nodes
        distance = tspData.get_cost_distance(solution[len(solution)-1], freenode2.nodeId)
        pheromone = tspData.get_pheromone(solution[len(solution)-1], freenode2.nodeId)
        tauAlpha = pheromone ** self.alpha
        NruBeta = (1/distance) ** self.beta
        costSum += tauAlpha * NruBeta

      for freenode2 in freeNodestmp:
        # Calculate teh cost of each node
        distance = tspData.get_cost_distance(solution[len(solution)-1], freenode2.nodeId)
        pheromone = tspData.get_pheromone(solution[len(solution)-1], freenode2.nodeId)
        tauAlpha = pheromone ** self.alpha
        NruBeta = (1/distance) ** self.beta
        cost = (tauAlpha * NruBeta) / costSum
        if cost > maxCost or nextNode == None:
          maxCost = cost
          nextNode = freenode2
      solution.append(nextNode.nodeId)
      freeNodestmp.discard(nextNode)
      freeNodes = freeNodestmp
    return solution

      

  def local_search(self, solution):
    return solution

  def apply_pheromone(self, tspData, solutions):
    q = 2  # Pheromone constant
    tspData.evaporate_pheromone(self.decay)
    solutions.append(self.bestSolution)
    for solution in solutions:
      distance = calculate_path_distance(solution, tspData)
      prevNode = None
      currNode = None
      for node in solution:
        if prevNode is None:
          prevNode = node
          continue
        currNode = node

        currValue = tspData.get_pheromone(currNode, prevNode)
        currValue += q/distance
        tspData.set_pheromone(currNode, prevNode, currValue)



# helper function that finds best path distance from list of solutions
def update_best_solution( bestSolution, bestDist, solutions, tspData):
  for solution in solutions:
    distance = calculate_path_distance(solution, tspData)
    if distance < bestDist or bestSolution == None:
      bestSolution = solution
      bestDist = distance
  return bestSolution, bestDist

import logging
import os
import random
import sys

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, '..', 'Support'))
from TspData import TspData
from TspData import calculate_path_distance

def MMACO(tspData, numOfAnts=2, numberOfAttempts = 20, pheromoneDecay=0.9):
  global decay 
  decay = pheromoneDecay
  inc = 0
  bestSolution = None
  bestDist = float('inf')
  logging.info(f"runnging for {numberOfAttempts} attempts")
  while(True):
    solutions = []
    for i in range(numOfAnts):
      # Select a random starting point
      solutions.append([random.randint(1,tspData.dimension)])
    for i in range(numOfAnts):
      solutions[i] = tour_construct_solution( tspData, solutions[i])
      solutions[i] = local_search(solutions[i])
    bestSolution, bestDist = update_best_solution(bestSolution, bestDist, 
                                                  solutions, tspData)
    apply_pheromone(tspData, solutions, bestDist)

    #temp
    if inc > numberOfAttempts:
      break
    if inc % 20 == 0:
      logging.info(f"attempt: {inc} best distance: {bestDist}")

    inc += 1
  return bestSolution, bestDist

def tour_construct_solution(tspData, solution):
  if len(solution) < 1:
    logging.error(f"this should not happen")
    return
  freeNodes = set(tspData.nodes)
  for freeNode1 in freeNodes:
    if freeNode1.nodeId == solution[0]:
      freeNodes.discard(freeNode1)
      break

  # build greedy MST
  logging.debug("pheromone\n" + tspData.pheromone_to_string())
  logging.debug("cost\n" + tspData.cost_to_string())
  solutionDistanceSum = 0
  for i in range(len(freeNodes)): # n-1 runs to create a spanning tree
    logging.debug(f"i: {i}")
    maxCost = 0
    maxCosts_distance = 0
    nextNode = None
    for freenode2 in freeNodes:
      beta = 2
      alpha = 1
      q0 = 0.85
      q = random.uniform(0, 1)
      distance = tspData.get_cost_distance(solution[len(solution)-1], freenode2.nodeId)
      pheromone = tspData.get_pheromone(solution[len(solution)-1], freenode2.nodeId)
      tauAlpha = pheromone ** alpha
      NruBeta = (1/distance) ** beta
      cost = pheromone * NruBeta
      if  q <= q0:
        if solutionDistanceSum > 0 and cost > 0:
          tempDistanceCost = solutionDistanceSum + distance
          cost/(tempDistanceCost*cost)
        else:
          cost = 0
      if cost > maxCost or nextNode == None:
        maxCost = cost
        maxCosts_distance = distance
        nextNode = freenode2
    solutionDistanceSum += maxCosts_distance
    solution.append(nextNode.nodeId)
    freeNodes.discard(nextNode)
  return solution


    

def local_search(solution):
  return solution

def apply_pheromone(tspData, solutions, bestDistance):
  q = 1  # Pheromone constant
  tspData.evaporate_pheromone(decay)
  prevNode = None
  currNode = None
  for solution in solutions:
    distance = calculate_path_distance(solution, tspData)
    for node in solution:
      if prevNode is None:
        prevNode = node
        continue
      currNode = node

      currValue = tspData.get_pheromone(currNode, prevNode)
      currValue += q/distance
      tmax = decay * q/distance
      if currValue > tmax:
        currValue = tmax
      tspData.set_pheromone(currNode, prevNode, currValue)



def update_best_solution(bestSolution, bestDist, solutions, tspData):
  for solution in solutions:
    distance = calculate_path_distance(solution, tspData)
    if distance < bestDist or bestSolution == None:
      bestSolution = solution
      bestDist = distance
  return bestSolution, bestDist

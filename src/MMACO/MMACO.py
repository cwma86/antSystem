import logging
import random
from TspData import TspData

def MMACO(tspData, numOfAnts=2, numberOfAttempts = 20):
  inc = 0
  bestSolution = None
  while(True):
    solutions = []
    for i in range(numOfAnts):
      solutions.append([random.randint(1,tspData.dimension)])
    for i in range(numOfAnts):
      solutions[i] = tour_construct_solution( tspData, solutions[i])
      solutions[i] = local_search(solutions[i])
    bestSolution = update_best_solution(bestSolution, solutions, tspData)
    apply_pheromone(tspData, bestSolution)

    #temp
    if inc > numberOfAttempts:
      break
    if inc % 2 == 0:
      logging.info("best solution")
      stringOut = ""
      for i in range(len(bestSolution)):
        stringOut += (f"node[{i}]: {bestSolution[i]}, ")
      logging.info(f"best solution: \n {stringOut}")

    inc += 1
  return bestSolution

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
  isEven = False
  logging.debug("pheromone\n" + tspData.pheromone_to_string())
  logging.debug("cost\n" + tspData.cost_to_string())
  for i in range(len(freeNodes)): # n-1 runs to create a spanning tree
    logging.debug(f"i: {i}")
    smallestDist = float("inf")
    LargestPheromone = float("-inf")
    nextNode = None
    for freenode2 in freeNodes:
      if isEven:
        distance = tspData.get_cost_distance(solution[len(solution)-1], freenode2.nodeId)
        if distance < smallestDist or nextNode == None:
          smallestDist = distance
          nextNode = freenode2
      else:
        pheromone = tspData.get_pheromone(solution[len(solution)-1], freenode2.nodeId)
        if pheromone > LargestPheromone or nextNode == None:
          LargestPheromone = pheromone
          nextNode = freenode2
    solution.append(nextNode.nodeId)
    freeNodes.discard(nextNode)
    if isEven:
      isEven = False
      logging.debug("\n" + tspData.pheromone_to_string())
    else:
      isEven = True
  return solution


    

def local_search(solution):
  return solution

def apply_pheromone(tspData, solution):
  tspData.evaporate_pheromone()
  prevNode = None
  currNode = None
  for node in solution:
    if prevNode is None:
      prevNode = node
      continue
    currNode = node

    currValue = tspData.get_pheromone(currNode, prevNode)
    currValue += 1/tspData.get_cost_distance(currNode, prevNode)
    tspData.set_pheromone(currNode, prevNode, currValue)



def update_best_solution(bestSolution, solutions, tspData):
  bestDistance = float("inf")
  if not bestSolution is None:
    bestDistance = calculate_path_distance(bestSolution, tspData)

  for solution in solutions:
    distance = calculate_path_distance(solution, tspData)
    if distance < bestDistance or bestSolution == None:
      bestSolution = solution
      bestDistance = distance
  return bestSolution

def calculate_path_distance(solution, tspData):
    distance = 0
    firstNode = None
    currNode = None
    prevNode = None
    for node in solution:
      if prevNode == None:
        firstNode = node
        prevNode = firstNode
        continue
      currNode = node
      distance += tspData.get_cost_distance(currNode, prevNode)
      prevNode = currNode
    # add the distance back to the initial node
    distance += tspData.get_cost_distance(firstNode, currNode)
    return distance


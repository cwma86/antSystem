import logging
import os
import sys
from random import choice

from MonteCarloTSNode import MonteCarloTSNode

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, '..', 'Support'))
from TspData import TspData
from TspData import calculate_path_distance
from TspData import calculate_pheromone_sum


class MonteCarloAntColonyNode(MonteCarloTSNode):
  """class for MonteCarloAntColony

  class for MonteCarloAntColony

  """
  def __init__(self, tspData, solutionList, freeNodesList, bestSolution):
    self.tspData = tspData
    self.solutionList = solutionList
    self.freeNodesList = freeNodesList
    self.bestSolution = bestSolution
    self.alpha = 4.0
    self.beta = 4.0

  def _findChildNodes(self):
    """ Find all Child nodes

    Get all child node positions

    Returns:
      set: A list of child node positions
    """
    childNodes = set()
    if self._isTerminalNode():
      return childNodes  # Game over, no children

    for i in self.freeNodesList:
      newSolution = []
      for j in self.solutionList:
        newSolution.append(j)
      newSolution.append(i.nodeId)
      childNodes.add(self.__make_move(newSolution))

    return childNodes


  def _findRandomChild(self):
    """ Find a random child

    Find a random child

    Returns:
      MonteCarloTSNode: instance of the object in child state
    """
    if self._isTerminalNode():
      return None  # Game over, no children

    # Randomly select one of the children
    solutionNodes = []
    nextNode = choice(self.freeNodesList)
    for j in self.solutionList:
      solutionNodes.append(j)
    solutionNodes.append(nextNode.nodeId)

    return self.__make_move(solutionNodes)


  def _isTerminalNode(self):
    """ Determine if the search is over

    Determine if the search is over 

    Returns:
      bool: A bool representing if the search is over
    """
    if len(self.freeNodesList) <= 0 :
      return True
    else:
      return False

  def _getReward(self):
    """ Calculate the reward of the current node state

    Calculate the reward of the current node state. 

    Returns:
      float: value of the reward between -1.0 and 1.0
    """
    costSum = 0
    distSum = 0
    firstNode = None
    prevNode = None
    currNode = None
    for node in self.solutionList:
      if prevNode == None:
        firstNode = node
        prevNode = firstNode
        continue
      currNode = node
      distance = self.tspData.get_cost_distance(currNode, prevNode)
      distSum += distance
      pheromone = self.tspData.get_pheromone(currNode, prevNode)
      tauAlpha = pheromone ** self.alpha
      NruBeta = (1/distance) ** self.beta
      costSum += tauAlpha * NruBeta
    
    distance = self.tspData.get_cost_distance(currNode, firstNode)
    pheromone = self.tspData.get_pheromone(currNode, firstNode)
    tauAlpha = pheromone ** self.alpha
    NruBeta = (1/distance) ** self.beta
    costSum += tauAlpha * NruBeta

    bestcostSum = 0.0 
    bestdistanceSum = 0.0
    if self.bestSolution == None:
      bestcostSum = costSum * 2
      bestdistanceSum = float("inf")
    else:
      bestcostSum = 0
      firstNode = None
      prevNode = None
      currNode = None
      for node in self.bestSolution:
        if prevNode == None:
          firstNode = node
          prevNode = firstNode
          continue
        currNode = node
        distance = self.tspData.get_cost_distance(currNode, prevNode)
        bestdistanceSum += bestdistanceSum
        pheromone = self.tspData.get_pheromone(currNode, prevNode)
        tauAlpha = pheromone ** self.alpha
        NruBeta = (1/distance) ** self.beta
        bestcostSum += tauAlpha * NruBeta
      
      bestdistance = self.tspData.get_cost_distance(currNode, firstNode)
      bestpheromone = self.tspData.get_pheromone(currNode, firstNode)
      besttauAlpha = bestpheromone ** self.alpha
      bestNruBeta = (1/bestdistance) ** self.beta
      bestcostSum += besttauAlpha * bestNruBeta

    rewardSum = 0.0
    if costSum > bestcostSum:
      rewardSum += 1.0
    # if distSum < bestdistanceSum:
    #   rewardSum += 0.5
    return rewardSum


  def __make_move(self, solutionNodes):
    """ Execute a move

    Execute a move

    Returns:
      MonteCarloAntColonyNode: a board representation after your move
    """
    newFreeList = self.freeNodesList.copy()
    if len(solutionNodes) >= 1:
      for node in newFreeList:
        if solutionNodes[len(solutionNodes)-1] == node.nodeId:
          newFreeList.remove(node)
          break
    return MonteCarloAntColonyNode(self.tspData, solutionNodes, newFreeList, self.bestSolution)
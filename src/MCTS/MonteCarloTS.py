# Class structure and functionality inspired by https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
from collections import defaultdict
import logging
import math
from typing import List


class MonteCarloTS:
    """MonteCarloTS
    This Monte Carlo Tree Search class provides an implementation of the 
    algorithm so that future objects can make use of it by implementing the 
    methods defined in MonteCarloTSNode and then calling the public methods 
    selectBestNode and simulate
    Attributes:
        reward: a dictionary of nodes and reward values for each
        count: a dictionary of nodes and # of visits to them
        childNode: a dictionary of each possible child nodes
        childNode: a dictionary of each possible child nodes
        weight: exploration parameter. Theoretical sqrt(2), but should be chosen empirically
    """
    def __init__(self, explorParam=math.sqrt(2)):
      """MonteCarlo tree search constructor
        MonteCarlo tree search constructor
      Args:
        weight: exploration parameter. Theoretical sqrt(2), but should be chosen empirically
      Returns:
        a MonteCarloTS object
      """
      self.reward = defaultdict(int)
      self.count = defaultdict(int)
      self.childNode = dict()
      self.explorParam = explorParam

    def selectBestNode(self, node):
      """Select the best available node
        Select the best available node, based on max score as calculated by
        the ratio of reward value and visit count
      Args:
        node: The node at wich the best available child shall be selected from
      Returns:
        node: The node with the highest score value
      """
      if node._isTerminalNode():
        raise RuntimeError(f"selectBestNode() called on terminal node {node}")

      if node not in self.childNode:
        return node._findRandomChild()
      
      # Calculate the max score of all children
      maxScore = float("-inf")
      maxChildNode = None
      for childNode in self.childNode[node]:
        tmpScore =  float("-inf")
        if not self.count[childNode] == 0:
          tmpScore = self.reward[childNode] / self.count[childNode]

        if maxChildNode == None or tmpScore > maxScore:
          maxChildNode = childNode
          maxScore = tmpScore
      return maxChildNode

    def simulate(self, node):
      """Simulate possible paths through the tree
        Simulate possible paths through the tree 
      Args:
        node: The node at wich we are simulating from
      """
      path = self.__select(node)
      leaf = path[-1]
      self.__expand(leaf)
      reward = self.__simulate(leaf)
      self.__backup(path, reward)

    def __select(self, node):
      """Select the node with the best UCB
        Select the node with the highest upper confidence bound
      Args:
        node: The node at wich we are selecting
      """
      path = []
      while True:
        path.append(node)
        if node not in self.childNode or not self.childNode[node]:
          return path # unexplored or terminal Node

        unexplored = self.childNode[node] - self.childNode.keys()
        if unexplored:
          n = unexplored.pop()
          path.append(n)
          return path

        node = self.__upperConfBound(node) 

    def __expand(self, node):
      """expand the node
        expand the node by finding all childe nodes
      Args:
        node: The node at which shall be expanded
      """
      if node in self.childNode:
        return  # already expanded
      self.childNode[node] = node._findChildNodes()


    def __simulate(self, node):
      """Simulate
        Simulate for best possible choice
      Args:
        node: The node at which shall be simulated
      Returns:
        float: The reward value
      """
      invert_reward = True
      while True:
        if node._isTerminalNode():
          reward = node._getReward()
          return 1 - reward if invert_reward else reward
        node = node._findRandomChild()
        invert_reward = not invert_reward

    def __backup(self, path, reward):
      """backup
        move back up the tree 
      Args:
        path: path of nodes
        reward: value of the reward from root 
      Returns:
        float: The reward value
      """
      for node in reversed(path):
        self.count[node] += 1
        self.reward[node] += reward
        reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa


    def __upperConfBound(self, node):
      """Calculate the upper confidence Bound 
        Calculate the upper confidence Bound using Wi/Ni + c sqrt(ln(Ni)/ni)
        where,
          Wi = reward of the child
          Ni = count of the parent
          c = explorationParameter
          ni = count of the child
      Args:
        path: path of nodes
        reward: value of the reward from root 
      Returns:
        float: The reward value
      """
      assert all(n in self.childNode for n in self.childNode[node])

      log_N_vertex = math.log(self.count[node])
      
      UCB = None
      maxChildNode = None
      for childNode in self.childNode[node]:
        Xi= self.reward[childNode] / self.count[childNode]
        c = self.explorParam
        tmpUCB = Xi + c * math.sqrt(log_N_vertex / self.count[childNode])
        if UCB == None or tmpUCB > UCB:
          UCB = tmpUCB
          maxChildNode = childNode
      return maxChildNode
# Class structure and functionality inspired by https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
from collections import defaultdict
import logging
import math

from MonteCarloTS import MonteCarloTS


class MonteCarloTSmod(MonteCarloTS):

    def _MonteCarloTS__simulate(self, node):
      """Simulate

        Simulate for best possible choice

      Args:
        node: The node at which shall be simulated

      Returns:
        float: The reward value
      """
      invert_reward = False
      while True:
        if node._isTerminalNode():
          reward = node._getReward()
          return 1 - reward if invert_reward else reward
        node = node._findRandomChild()
    def _MonteCarloTS__upperConfBound(self, node):
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

# Class structure inspired by https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
from abc import ABC, abstractmethod


class MonteCarloTSNode(ABC):
  """Abstract class for MonteCarlo tree search nodes

  Abstract class for MonteCarlo tree search nodes, that provides the signature
  of object required to use the monte Carlo tree search

  """
  @abstractmethod
  def _findChildNodes(self):
    """ Find all Child nodes

    Get all child node positions

    Returns:
      set: A list of child node positions
    """
    return set()

  @abstractmethod
  def _findRandomChild(self):
    """ Find a random child

    Find a random child

    Returns:
      MonteCarloTSNode: instance of the object in child state
    """
    return None

  @abstractmethod
  def _isTerminalNode(self):
    """ Determine if the search is over

    Determine if the search is over 

    Returns:
      bool: A bool representing if the search is over
    """
    return True

  @abstractmethod
  def _getReward(self):
    """ Calculate the reward of the current node state

    Calculate the reward of the current node state. 

    Returns:
      float: value of the reward between -1.0 and 1.0
    """
    return 0

import logging
import math
import os
import sys

from SymetricMatrix import SymetricMatrix
from TspDataNode import TspDataNode

class TspData:
  def __init__(self, name="", comment="", type="",
               dimension=0, edgeWeight="" , nodes=[]):
    self.name = name
    self.comment = comment
    self.type = type
    self.dimension = dimension
    self.edgeWeight = edgeWeight
    self.nodes = nodes
    self.cost = SymetricMatrix(self.dimension, initialValue=float("inf"))
    self.pheromone = SymetricMatrix(self.dimension, initialValue=0.0)
 

  def header_to_string(self):
    headerStr = (f"header, name:{self.name} comment:{self.comment} "
                  f"type:{self.type} dimension:{self.dimension} " 
                  f"edge:{self.edgeWeight}")
    return headerStr


  def data_to_string(self):
    dataStr = "Data: \n"
    for node in self.nodes:
      dataStr += (f" nodeId:{node.nodeId} x: {node.xCoord} "
                   f"y: {node.yCoord}\n")
    return dataStr


  def get_cost_distance(self, fromIndex, to):
    ''' uses index 1 matrix locations'''
    if fromIndex == to:
      return float("inf")
    value = self.cost.get_value(fromIndex, to)
    if value == float("inf"):
      # Value is not yet set, calculate it
      value = math.dist([self.nodes[fromIndex-1].xCoord,self.nodes[fromIndex-1].yCoord],
                        [self.nodes[to-1].xCoord,self.nodes[to-1].yCoord])
      self.cost.set_value(fromIndex, to, value)
    return value
    

  def get_pheromone(self, fromIndex, to):
    return self.pheromone.get_value(fromIndex, to)


  def evaporate_pheromone(self):
    ''' uses index 1 matrix locations'''
    decay = 0.1
    for node in self.pheromone.matrix:
      node = (1-decay) * node    

  def set_pheromone(self, fromIndex, to, value):
    self.pheromone.set_value(fromIndex, to, value)

  def pheromone_to_string(self):
    return self.pheromone.to_string()

  def cost_to_string(self):
    return self.cost.to_string()

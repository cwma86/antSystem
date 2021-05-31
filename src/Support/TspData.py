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
    self.pheromone = SymetricMatrix(self.dimension, initialValue=0.000001)
 

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


  def evaporate_pheromone(self, decay):
    ''' uses index 1 matrix locations'''
    for node in self.pheromone.matrix:
      node = decay * node    

  def adjust_max_pheromone(self, maxValue):
    ''' uses index 1 matrix locations'''
    for node in self.pheromone.matrix:
      if node > maxValue:
        node = maxValue    

  def set_pheromone(self, fromIndex, to, value):
    self.pheromone.set_value(fromIndex, to, value)

  def pheromone_to_string(self):
    return self.pheromone.to_string()

  def cost_to_string(self):
    return self.cost.to_string()

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

def calculate_pheromone_sum(solution, tspData):
    pheroSum = 0
    firstNode = None
    currNode = None
    prevNode = None
    for node in solution:
      if prevNode == None:
        firstNode = node
        prevNode = firstNode
        continue
      currNode = node
      pheroSum += tspData.get_pheromone(currNode, prevNode)
      prevNode = currNode
    # add the pheroSum back to the initial node
    pheroSum += tspData.get_pheromone(firstNode, currNode)
    return pheroSum




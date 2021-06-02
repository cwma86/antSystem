import logging
import os
import sys

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, '..', 'Support'))
from TspParser import TspParser
from TspData import calculate_path_distance


def brute_force_solution(tspData):
  minDist = float('inf')
  minPath = None
  counter = 0 
  startNodeSet = set()
  for node in tspData.nodes:
    startNodeSet.add(node.nodeId)
  startPoint = startNodeSet.pop()
  for node in startNodeSet:
    nodeSet = set(startNodeSet.copy())
    nodeSet.remove(node)
    paths = find_all_paths(nodeSet)
    tempNodes = [node]
    for path in paths:
      distancePath = [startPoint]
      distancePath.append(node)
      for tmpNode in path:
        distancePath.append(tmpNode)
      if len(distancePath) < 10:
        logging.error("this shouldn't happen")
      dist = calculate_path_distance(distancePath, tspData)
      if dist < minDist or minPath == None:
        minDist = dist
        minPath = distancePath 
      if counter % 10000 == 0:
        logging.debug(f"counter[{counter}]best solution distance {minDist}")
      counter +=1
  return minPath, minDist



def find_all_paths(nodes):
  paths = []
  if len(nodes) == 0:
    logging.error("shit something is wrong")
    return paths
  if len(nodes) == 1:
    path = [nodes.pop()]
    paths.append(path)
    return paths
  for node in nodes:
    nodeSet = set(nodes.copy())
    nodeSet.remove(node)
    childPaths = find_all_paths(nodeSet)
    for childPath in childPaths:
      newPath = [node]
      for childNode in childPath:
        newPath.append(childNode)
      paths.append(newPath)
  return paths

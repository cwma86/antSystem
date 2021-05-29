#!/usr/bin/env python3
import argparse
import logging
import math
import os
import sys

script_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(script_path, '..', 'MMACO'))
from TspParser import TspParser
from MMACO import calculate_path_distance

def args():
  defaultFilePath = os.path.join(script_path, '..', '..', 'TSPData','pcb10_test.tsp')
  parser = argparse.ArgumentParser(description='Run Ant System')   
  parser.add_argument('--filename', default=defaultFilePath, type=str,
                      help='file path of tsp data')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='verbose logging')
  args = parser.parse_args()

  # initialize logger format
  logLevel = logging.INFO
  if args.verbose:
    logLevel = logging.DEBUG
  logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s\
       [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logLevel)
  logging.debug(f"logging set to {logging.DEBUG}")
  logging.info(f"script_path: {script_path}")

  return args


def main(inputargs):
  # Get data from file
  tspData = TspParser(inputargs.filename)
  logging.debug(f"{len(tspData.nodes)} nodes created")
  logging.debug(tspData.data_to_string())
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
        logging.info(f"counter[{counter}]best solution distance {minDist}")
      counter +=1
  
  for i in reversed(range(len(minPath))):
    print(f"node[{i}]: {minPath[i]} ")
  print(f"best solution distance {minDist}")



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

if __name__ == "__main__":
  inputargs = args()
  main(inputargs)

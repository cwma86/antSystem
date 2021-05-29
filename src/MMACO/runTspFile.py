#!/usr/bin/env python3
import argparse
import logging
import os

from MMACO import MMACO
from SymetricMatrix import SymetricMatrix
from TspParser import TspParser
script_path = os.path.dirname(os.path.abspath( __file__ ))

def args():
  defaultFilePath = os.path.join(script_path, '..', '..', 'TSPData','lin318.tsp')
  parser = argparse.ArgumentParser(description='Run Ant System')   
  parser.add_argument('--filename', default=defaultFilePath, type=str,
                      help='file path of tsp data')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='verbose logging')
  parser.add_argument('-a', '--workerAntCount', type=int, 
                      help='The amount of Worker Ants to crawl '
                        + 'the food sources and leave pheromone trails')
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
  bestSolution = MMACO(tspData)
  for i in range(len(bestSolution)):
    print(f"node[{i}]: {bestSolution[i]}")
  
if __name__ == "__main__":
  inputargs = args()
  main(inputargs)

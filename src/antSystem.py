#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from TspGraphReader import TspGraphReader

script_path = os.path.dirname(os.path.abspath( __file__ ))

def args():
  defaultFilePath = os.path.join(script_path, '../TSPData/pla85900.tsp')
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
  tspGraph = TspGraphReader(filename=inputargs.filename)
  if tspGraph == None:
    logging.error(f"Failed to construct TspGraphReader")
    sys.exit(1)


if __name__ == "__main__":
  inputargs = args()
  main(inputargs)
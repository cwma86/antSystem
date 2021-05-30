import logging
import os
import sys

from TspData import TspData
from TspDataNode import TspDataNode

def TspParser(filePath):
    tspData = None
    if not os.path.isfile(filePath):
      logging.error(f"Invalid file path: filePath")
      # TODO change to return None on construction instead of exit
      sys.exit(1)
    
    with open(filePath, 'r') as tspFile:
      tspData = parse_header(tspFile, tspData)
      parse_data(tspFile, tspData)
    return tspData

def parse_header(tspFile, tspData):
  logging.debug(f"getting header")
  name = ""
  comment = ""
  type = ""
  dimension = int()
  for i in range(5):
    # Name
    line = tspFile.readline().split(":")
    dataItem =  "name"
    if line[0].strip().lower() == dataItem:
      name = line[1].strip()

    # Comment
    dataItem =  "comment"
    if line[0].strip().lower() == dataItem:
      comment = line[1].strip()

    # Type
    dataItem =  "type"
    if line[0].strip().lower() == dataItem:
      type = line[1].strip()
    # Dimension
    dataItem =  "dimension"
    if line[0].strip().lower() == dataItem:
      try:
        dimension = int(line[1].strip())
      except ValueError:
        logging.error(f"Invalid header, expected {dataItem} but value is not an int '{line[0].strip().lower()}'")
        return

    # Edge weight
    dataItem =  "edge_weight_type"
    if line[0].strip().lower() == dataItem:
      edgeWeight = line[1].strip()

    # Node section (not data just skip)     
  line = tspFile.readline().split(":")
  tspData = TspData(name, comment, type,
               dimension, edgeWeight)
  logging.debug(tspData.header_to_string())
  return tspData


def parse_data(tspFile, tspData):
  logging.debug(f"getting data")
  for node in range(0,tspData.dimension):
    line = tspFile.readline().split()
    try:
      nodeId = int(line[0])
    except ValueError:
      logging.error(f"Invalid nodeId: {line[0]} is not an int")
      return
    try:
      xcoord=float(line[1])
    except ValueError:
      logging.error(f"Invalid xcoord: {line[1]} is not an float")
      return
    try:
      ycoord=float(line[2])
    except ValueError:
      logging.error(f"Invalid ycoord: {line[1]} is not an float")
      return
    tspData.nodes.append(TspDataNode(nodeId, xcoord, ycoord))



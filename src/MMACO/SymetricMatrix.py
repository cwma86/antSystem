import multiprocessing
import logging

class SymetricMatrix():
  def __init__(self, size, initialValue=float("inf")):
    ''' given a sizes creates a square  where the cost from a node to 
        it's self is 'ini' and all other costs are '-inf'

        indexing starts at 1
    '''
    self.size = size
    self.numOfNodes = (size + 1) * size // 2
    logging.debug(f"numOfNodes{self.numOfNodes}")
    self.matrix = multiprocessing.Array('d', range(self.numOfNodes))
    #Initialize the cost of all nodes to inf
    for i in range(self.numOfNodes):
      self.matrix[i] = initialValue

  
  def _get_index(self, row, col):
    if col > row:
      tmpRow = row
      row = col
      col = tmpRow
    index = (0+row) * (row + 1) // 2 + col
    return index
  
  def get_value(self, row, col):
    row -= 1
    col -= 1
    index = self._get_index(row, col)
    value = self.matrix[index]
    return value

  def set_value(self, row, col, value):
    row -= 1
    col -= 1
    index = self._get_index(row, col)
    self.matrix[index] = value 

  def to_string(self):
    outStr = ""
    for i in range(1, self.size+1):
      for j in range(1, self.size+1):
        outStr += (f"{self.get_value(i,j):.4f} ")
      outStr += (f"\n")
    return outStr








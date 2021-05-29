#!/usr/bin/env python3
import logging
import os
import sys
import unittest

script_path = os.path.dirname(os.path.abspath( __file__ ))
src_dir = os.path.join(script_path, "..","src", "MMACO")
sys.path.insert(1, src_dir)
from SymetricMatrix import SymetricMatrix

logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s\
                [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.DEBUG)

class test_SymetricMatrix(unittest.TestCase):
  def test_SymetricMatrix(self):
    # Validate Initialization
    matrix = SymetricMatrix(5)
    retValue = matrix.get_value(1,1)
    self.assertEqual(retValue, float("inf"))

    # Validate set value
    setValue = 2.0
    matrix.set_value(1,1, setValue)
    retValue = matrix.get_value(1,1)
    self.assertEqual(retValue, setValue)

    # Validate node symetry
    setValue = 82.0
    matrix.set_value(1,5, setValue)
    retValue = matrix.get_value(5,1)
    self.assertEqual(retValue, setValue)



if __name__ == '__main__':
    unittest.main()
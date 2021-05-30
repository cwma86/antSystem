#!/usr/bin/env python3

# tic tac toe logic from https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
import logging
import os
import sys
import unittest
from collections import namedtuple
from random import choice

script_path = os.path.dirname(os.path.abspath( __file__ ))
src_dir = os.path.join(script_path, "..","src","MCTS")
sys.path.insert(1, src_dir)
from MonteCarloTS import MonteCarloTS
from MonteCarloTSNode import MonteCarloTSNode

logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s\
                [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)

# named tuple (class name, Constructor arguments )
_TicTacToe = namedtuple("TicTacToeBoard", "tup turn winner terminal")
class TicTacToeBoard(_TicTacToe, MonteCarloTSNode):
  """Tic Tac Toe board example class

  This is an example TicTacToe board to be used as a reference implementation
  of our monteCarlo tree search algorithm
    1 2 3
  1 - - -
  2 - - -
  3 - - -

  Attributes:
      tup: A tuple indicating each board location.
      turn: A Bool indicating if it is the players turn.
      winner: A Bool indicating the winner. None if no winner, True if X wins, False if O wins
      terminal: a Bool that indicates true if no more moves can be made.
  """
  def _winning_combos(self):
    """Returns Winning board combos

    returns a list of winning positions on the board as represented by 

    0 1 2
    3 4 5
    6 7 8

    Returns:
        winningPositions: a list of all winning combinations
    """ 
    winningPositions = [] 
    for start in range(0, 9, 3):
      winningPositions.append((start, start + 1, start + 2))
    for start in range(3):
      winningPositions.append((start, start + 3, start + 6))
    winningPositions.append((0, 4, 8))
    winningPositions.append((2, 4, 6))
    return winningPositions


  def _find_winner(self, tup):
    """Check for winner.

    Inspect all positions on the board and determine if there is a winner

    Args:
      tup: a tuple representation of the board

    Returns:
      bool: A bool representation of the winner. True X wins, False O wins, and None no winner
    """
    for i1, i2, i3 in self._winning_combos():
      v1, v2, v3 = tup[i1], tup[i2], tup[i3]
      if False is v1 is v2 is v3:
        return False
      if True is v1 is v2 is v3:
        return True
    return None
      
  def _findChildNodes(self):
    """ Find all Child nodes

    Get all child board positions

    Returns:
      set: A list of child board positions
    """
    childNodes = set()
    if self.terminal:
      return childNodes  # Game over, no children

    for i, value in enumerate(self.tup):
      if value is None:
        childNodes.add(self.__make_move(i))
    return childNodes


  def _findRandomChild(self):
    """ Find a random child

    Find a random child

    Returns:
      TicTacToeBoard: A board selected at random from potential children
    """
    if self.terminal:
      return None  # Game over, no children
    empty_spots = []
    for i, value in enumerate(self.tup):
      if value is None:
        empty_spots.append(i)
    
    # Randomly select one of the children
    nextMove = choice(empty_spots)

    return self.__make_move(nextMove)

  def _getReward(self):
    """ Calculate the reward of the current board state

    Calculate the reward of the current board state. 

    Returns:
      float: value of the reward between -1.0 and 1.0
    """
    if self.winner is None:
      return 0.5  # tie
    if self.turn is (not self.winner):
      return -1.0  # You Lose

  def _isTerminalNode(self):
    """ Determine if the game is over

    Determine if the game is over 

    Returns:
      bool: A bool representing if the game is over
    """
    return self.terminal

  def __make_move(self, index):
    """ Execute a move

    Execute a move

    Returns:
      TicTacToeBoard: a board representation after your move
    """
    tup = self.tup[:index] + (self.turn,) + self.tup[index + 1 :]
    turn = not self.turn
    winner = self._find_winner(tup)
    isTerminalNode = (winner is not None) or not any(v is None for v in tup)
    return TicTacToeBoard(tup, turn, winner, isTerminalNode)

  def to_string(self):
    """ String representation of the board 

    String representation of the board 
      1 2 3
    1
    2
    3

    Returns:
      String representation of the board 
    """
    to_char = lambda v: ("X" if v is True else ("O" if v is False else " "))
    rows = [
      [to_char(self.tup[3 * row + col]) for col in range(3)] for row in range(3)
    ]
    return (
      "\n  1 2 3\n"
      + "\n".join(str(i + 1) + " " + " ".join(row) for i, row in enumerate(rows))
      + "\n"
    )

def play_game(simulationsToTrain=10):
  """ Play 1 game of tic tac toe

    Play 1 game of tic tac toe with 2 MoteCarlo simulated players 

  Arguments:
    simulationsToTrain: number of simulations that should be run prior to making a move
  Returns:
    xWin: int value if player x won
    oWin: int value if player o won
  """
  xWin = 0
  oWin = 0
  player1 = MonteCarloTS()
  player2 = MonteCarloTS()
  board = new_tic_tac_toe_board()
  logging.debug(board.to_string())
  while True:
      # Train player1
      for _ in range(simulationsToTrain):
          player1.simulate(board)
      board = player1.selectBestNode(board)
      logging.debug(board.to_string())
      if board.terminal:
        break

      # Train player2
      for _ in range(simulationsToTrain):
          player2.simulate(board)
      board = player2.selectBestNode(board)
      logging.debug(board.to_string())
      if board.terminal:
        break
  if board.winner == None:
    logging.debug(f"Draw")
  elif board.winner == True:
    logging.debug(f"Winner: player1 X ")
    xWin +=1
  else:
    logging.debug(f"Winner: player2 O")
    oWin +=1
  return xWin, oWin

def new_tic_tac_toe_board():
  """ Create a new Tic tac toe board

    Creates a new empty tic tac toe board


  Returns:
    TicTacToeBoard: returns an empty board object
  """
  return TicTacToeBoard(tup=(None,) * 9, turn=True, winner=None, terminal=False)

class test_TspGraph(unittest.TestCase):
  def test_invalidInputFile(self):
    attempts = 30
    xWin = 0
    oWin = 0
    for i in range(0, attempts):
      x, o = play_game(simulationsToTrain=200)
      xWin += x
      oWin += o
    logging.info(f"x wins: {xWin/attempts}")
    logging.info(f"o wins: {oWin/attempts}")
    logging.info(f"draw: {(attempts-(oWin+xWin))/attempts}")
    self.assertLess(xWin/attempts, 0.3)
    self.assertLess(oWin/attempts, 0.1)
    self.assertGreater((attempts-(oWin+xWin))/attempts, 0.7)

if __name__ == "__main__":
    unittest.main()

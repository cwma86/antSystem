import logging
import math
import os
import random
import sys

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, 'MCTS'))
from MonteCarloTreeNode import MCTSNode

class Underling:
    def __init__(self, environment):
        self.Environment = environment
        startingSpot = environment.FoodSources[0]
        self.StartingFoodSource = startingSpot
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = dict()  # FoodSource > visited order

    def execute_mcts(self):
        root = MCTSNode(self.Environment, None, self.CurrentFoodSource)

        parent = root

        logging.debug('Root Node Initial Info')
        logging.debug(f'Root Food Source ID: {parent.get_foodsource().FoodSourceId}')
        logging.debug(f'Root BEST: {parent.BestTourDistance}')
        logging.debug('')

        resources = 0
        TARGET = 50000
        while resources < TARGET:

            if(resources % 500 == 0):
                selectedNode = parent.select() #Expansion is included in this step

                logging.debug('Selected Node Initial Info')
                logging.debug(f'Depth Level {len(selectedNode.OngoingTour)}')
                logging.debug(f'Selected Food Source ID: {selectedNode.get_foodsource().FoodSourceId}')
                logging.debug('')

                if selectedNode.IsTerminalNode:
                    break

                tourScore, tourPath = selectedNode.rollout() # 'Simulate' is an equivalent term you'll see in MCTS articles
                logging.debug(f'Selected Node Tour Score: {tourScore}')
                logging.debug('')

                selectedNode.propagate(tourScore, tourPath)
                logging.debug('Root Node Info after Propagation')
                logging.debug(f'Root Food Source ID: {root.get_foodsource().FoodSourceId}')
                logging.debug(f'Root BEST: {root.BestTourDistance}')
                logging.debug(f'Root Best Rollout: {root.BestRollout}')
                logging.debug(f'Resources Remaining: {resources} of {TARGET}')
                logging.debug('')
            else:
                selectedNode = parent.select() #Expansion is included in this step

                # Check if terminal node
                if selectedNode.IsTerminalNode:
                    break

                (tourScore, tourPath) = selectedNode.rollout() # 'Simulate' is an equivalent term you'll see in MCTS articles
                selectedNode.propagate(tourScore, tourPath)

            # Step down to the best child after a sufficient amount of expansion.
            if (resources + 1) % (len(self.Environment.FoodSources) * 5) == 0:
                bestChild = self.__find_best_child(parent)
                if bestChild is None:
                    break
                logging.debug(f'Resources Used: {resources}')
                logging.debug(f'Stepping to the best child: {bestChild.CurrentFoodSource.FoodSourceId}')
                parent = bestChild
            
            resources += 1

        logging.debug(f'Finished')

        bestTour = root.BestRollout
        bestScore = self.Environment.score_tour(root.BestRollout)
        logging.info(f'Root Best Tour: {bestTour}')
        logging.info(f'Root Tour Score: {bestScore}')
        logging.info(f'MCTS Depth Analyzed: {len(selectedNode.OngoingTour)}')
        return bestTour, bestScore

    def __find_best_child(self, parentNode):
        bestChild = None
        bestChildScore = math.inf
        for child in parentNode.ChildNodes.values():
            if child.BestTourDistance < bestChildScore:
                bestChild = child
                bestChildScore = child.BestTourDistance

        return bestChild
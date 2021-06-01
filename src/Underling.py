import logging
import os
import random
import sys

file_path = os.path.dirname(os.path.abspath( __file__ ))
sys.path.append(os.path.join(file_path, 'MCTS'))
from MonteCarloTreeNode import MCTSNode

class Underling:
    def __init__(self, environment):
        self.Environment = environment
        startingSpot = environment.FoodSources[random.randrange(0, len(environment.FoodSources))]
        self.StartingFoodSource = startingSpot
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = dict()  # FoodSource > visited order

    def execute_mcts(self):
        mcts = MCTSNode(self.Environment, None, self.CurrentFoodSource)

        logging.info('Root Node Initial Info')
        logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
        logging.info(f'Root AVG: {mcts.AverageTourDistance}')
        logging.info(f'Root BEST: {mcts.BestTourDistance}')
        logging.info('')

        resources = 4000
        while resources > 0:

            if(resources % 400 == 0):
                selectedNode = mcts.select() #Expansion is included in this step
                logging.info('Selected Node Initial Info')
                logging.info(f'Node Level {len(selectedNode.OngoingTour)}')
                logging.info(f'Selected Food Source ID: {selectedNode.get_foodsource().FoodSourceId}')
                logging.info(f'Parent Food Source ID: {selectedNode.Parent.get_foodsource().FoodSourceId}')
                logging.info('')

                if selectedNode.IsTerminalNode:
                    break

                tourScore = selectedNode.rollout() # 'Simulate' is an equivalent term you'll see in MCTS articles
                logging.info(f'Tour Score: {tourScore}')
                logging.info('')

                selectedNode.propagate(tourScore)
                logging.info('Root Node Info after Propagation')
                logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
                logging.info(f'Root AVG: {mcts.AverageTourDistance}')
                logging.info(f'Root BEST: {mcts.BestTourDistance}')
                logging.info(f'Resources Remaining: {resources}')
                logging.info('')
            else:
                selectedNode = mcts.select() #Expansion is included in this step

                # Check if terminal node
                if selectedNode.IsTerminalNode:
                    break

                tourScore = selectedNode.rollout() # 'Simulate' is an equivalent term you'll see in MCTS articles
                selectedNode.propagate(tourScore)
            
            resources -= 1

        logging.info('Root Node Info after MCTS')
        logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
        logging.info(f'Root AVG: {mcts.AverageTourDistance}')
        logging.info(f'Root BEST: {mcts.BestTourDistance}')
        logging.info('')
import logging
import random
import math

from MonteCarloTreeNode import MCTSNode

class Underling:
    def __init__(self, environment):
        self.Environment = environment
        startingSpot = environment.FoodSources[random.randrange(0, len(environment.FoodSources))]
        self.StartingFoodSource = startingSpot
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = dict()  # FoodSource > visited order

    def execute_mcts(self):
        # mcts = MCTSNode(self.Environment, None, self.CurrentFoodSource, [self.CurrentFoodSource])

        # logging.info('Root Node Initial Info')
        # logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
        # logging.info(f'Root AVG: {mcts.AverageTourDistance}')
        # logging.info(f'Root BEST: {mcts.BestTourDistance}')
        # logging.info('')


        # selectedNode = mcts.select()

        # logging.info('Selected Node Initial Info')
        # logging.info(f'Selected Food Source ID: {selectedNode.get_foodsource().FoodSourceId}')
        # logging.info(f'Parent Food Source ID: {selectedNode.Parent.get_foodsource().FoodSourceId}')
        # logging.info(f'Selected AVG: {selectedNode.AverageTourDistance}')
        # logging.info(f'Selected BEST: {selectedNode.BestTourDistance}')
        # logging.info('')

        # tourScore = selectedNode.rollout()

        # logging.info(f'Tour Score: {tourScore}')
        # logging.info('')

        # selectedNode.propagate(tourScore)

        # logging.info('Root Node Info after Propagation')
        # logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
        # logging.info(f'Root AVG: {mcts.AverageTourDistance}')
        # logging.info(f'Root BEST: {mcts.BestTourDistance}')
        # logging.info('')

        # selectedNode = mcts.select()

        # logging.info('Selected Node Initial Info')
        # logging.info(f'Selected Food Source ID: {selectedNode.get_foodsource().FoodSourceId}')
        # logging.info(f'Parent Food Source ID: {selectedNode.Parent.get_foodsource().FoodSourceId}')
        # logging.info(f'Selected AVG: {selectedNode.AverageTourDistance}')
        # logging.info(f'Selected BEST: {selectedNode.BestTourDistance}')
        # logging.info('')

        # tourScore = selectedNode.rollout()

        # logging.info(f'Tour Score: {tourScore}')
        # logging.info('')

        # selectedNode.propagate(tourScore)

        # logging.info('Root Node Info after Propagation')
        # logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
        # logging.info(f'Root AVG: {mcts.AverageTourDistance}')
        # logging.info(f'Root BEST: {mcts.BestTourDistance}')
        # logging.info('')

        mcts = MCTSNode(self.Environment, None, self.CurrentFoodSource, [self.CurrentFoodSource])

        logging.info('Root Node Initial Info')
        logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
        logging.info(f'Root AVG: {mcts.AverageTourDistance}')
        logging.info(f'Root BEST: {mcts.BestTourDistance}')
        logging.info('')

        resources = 20
        while resources > 0:
            selectedNode = mcts.select()
            logging.info('Selected Node Initial Info')
            logging.info(f'Selected Food Source ID: {selectedNode.get_foodsource().FoodSourceId}')
            logging.info(f'Parent Food Source ID: {selectedNode.Parent.get_foodsource().FoodSourceId}')
            logging.info(f'Selected AVG: {selectedNode.AverageTourDistance}')
            logging.info(f'Selected BEST: {selectedNode.BestTourDistance}')
            logging.info('')

            tourScore = selectedNode.rollout()
            logging.info(f'Tour Score: {tourScore}')
            logging.info('')

            selectedNode.propagate(tourScore)
            logging.info('Root Node Info after Propagation')
            logging.info(f'Root Food Source ID: {mcts.get_foodsource().FoodSourceId}')
            logging.info(f'Root AVG: {mcts.AverageTourDistance}')
            logging.info(f'Root BEST: {mcts.BestTourDistance}')
            logging.info('')
            resources -= 1
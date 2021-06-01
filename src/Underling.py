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

        # self.Tour = [1, 2, 42, 43, 41, 46, 51, 44, 47, 52, 53, 105, 73, 69, 74, 81, 80, 68, 67, 71, 84, 83, 79, 82, 72, 77, 78]
        # self.TourNodes = []

        # if len(self.Tour) > 0:
        #     previousNode = MCTSNode(self.Environment, None, self.Environment.FoodSourceDict[self.Tour[0]])
        #     self.TourNodes.append(previousNode)
        #     for i in range(1, len(self.Tour)):
        #         currentNode = MCTSNode(self.Environment, previousNode, self.Environment.FoodSourceDict[self.Tour[i]], previousNode.OngoingTour)
        #         self.TourNodes.append(currentNode)
        #         previousNode = currentNode

        self.Tour = [self.CurrentFoodSource.FoodSourceId]

    def execute_mcts(self):
        parent = MCTSNode(self.Environment, None, self.CurrentFoodSource)

        logging.info('Root Node Initial Info')
        logging.info(f'Root Food Source ID: {parent.get_foodsource().FoodSourceId}')
        logging.info(f'Root AVG: {parent.AverageTourDistance}')
        logging.info(f'Root BEST: {parent.BestTourDistance}')
        logging.info('')

        while len(self.VisitedFoodSources) < len(self.Environment.FoodSources):
            resources = len(self.Environment.FoodSources) - len(self.Tour)
            while resources > 0:

                if(resources % 30 == 0):
                    selectedNode = parent.select() #Expansion is included in this step

                    if selectedNode is None:
                        i = 1

                    logging.info('Selected Node Initial Info')
                    logging.info(f'Node Level {len(selectedNode.OngoingTour)}')
                    logging.info(f'Selected Food Source ID: {selectedNode.get_foodsource().FoodSourceId}')
                    # logging.info(f'Parent Food Source ID: {selectedNode.Parent.get_foodsource().FoodSourceId}')
                    logging.info('')

                    if selectedNode.IsTerminalNode:
                        break

                    tourScore = selectedNode.rollout() # 'Simulate' is an equivalent term you'll see in MCTS articles
                    logging.info(f'Tour Score: {tourScore}')
                    logging.info('')

                    selectedNode.propagate(tourScore)
                    logging.info('Root Node Info after Propagation')
                    logging.info(f'Root Food Source ID: {parent.get_foodsource().FoodSourceId}')
                    logging.info(f'Root AVG: {parent.AverageTourDistance}')
                    logging.info(f'Root BEST: {parent.BestTourDistance}')
                    logging.info(f'Resources Remaining: {resources}')
                    logging.info('')
                else:
                    selectedNode = parent.select() #Expansion is included in this step

                    if selectedNode is None:
                        i = 1

                    # Check if terminal node
                    if selectedNode.IsTerminalNode:
                        break

                    tourScore = selectedNode.rollout() # 'Simulate' is an equivalent term you'll see in MCTS articles
                    selectedNode.propagate(tourScore)
                
                resources -= 1

            logging.info('Root Node Info after MCTS')
            logging.info(f'Root Food Source ID: {parent.get_foodsource().FoodSourceId}')
            logging.info(f'Root AVG: {parent.AverageTourDistance}')
            logging.info(f'Root BEST: {parent.BestTourDistance}')
            logging.info('')

            bestChild = self.__find_best_child(parent)

            if bestChild is None:
                break

            # self.TourNodes.append(bestChild)
            self.Tour.append(bestChild.CurrentFoodSource.FoodSourceId)

            parent = bestChild
            logging.info(f'Tour: {[i for i in self.Tour]}')

        logging.info(f'Finished')

        tour = [i for i in self.Tour]
        logging.info(f'Tour: {tour}')
        logging.info(f'Score: {self.Environment.score_tour(tour)}')

    def __find_best_child(self, parentNode):
        bestChild = None
        bestChildScore = math.inf
        for child in parentNode.ChildNodes.values():
            if child.AverageTourDistance < bestChildScore:
                bestChild = child
                bestChildScore = child.AverageTourDistance

        return bestChild
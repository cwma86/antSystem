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
        mcts = MCTSNode(self.Environment, None, self.CurrentFoodSource, [self.CurrentFoodSource])


        logging.info(f'Root Food Source: {mcts.get_foodsource().FoodSourceId}')
        logging.info(f'Root AVG: {mcts.AverageTourDistance}')
        logging.info(f'Root BEST: {mcts.BestTourDistance}')

        selectedNode = mcts.select()

        logging.info(f'Selected Food Source: {selectedNode.get_foodsource().FoodSourceId}')
        logging.info(f'Parent Food Source: {selectedNode.Parent.get_foodsource().FoodSourceId}')
        logging.info(f'Selected AVG: {selectedNode.AverageTourDistance}')
        logging.info(f'Selected BEST: {selectedNode.BestTourDistance}')

        tourScore = selectedNode.rollout()

        logging.info(f'Tour Score: {tourScore}')
        # selectedNode.propagate(tourScore)

        # resources = 20
        # while resources > 0:
        #     selectedNode = mcts.select()
        #     tourScore = selectedNode.rollout()
        #     selectedNode.propagate(tourScore)
        #     resources -= 1

    def complete_full_tour(self):
        self.VisitedFoodSources = dict()
        self.CurrentFoodSource = self.StartingFoodSource
        i = 0
        self.VisitedFoodSources[self.CurrentFoodSource] = i
        nextFoodSource = self.find_next()
        while nextFoodSource is not None:
            if nextFoodSource == self.StartingFoodSource:
                #Back to start
                break
            i += 1
            self.CurrentFoodSource = nextFoodSource
            self.VisitedFoodSources[self.CurrentFoodSource] = i
            nextFoodSource = self.find_next()

        pass

    def find_next(self):
        foodSourceToTrailList = self.Environment.FoodSourceDistances[self.CurrentFoodSource]

        smallestScore = float('inf')
        nextFoodSource = None
        for trailTuple in foodSourceToTrailList:
            if trailTuple not in self.Environment.PheromoneTrails:
                continue

            pheromoneScore = self.Environment.PheromoneTrails[trailTuple]
            score = self.heuristic(trailTuple[2], pheromoneScore)

            #Pick smallest score, but not the starting point, so we don't finish before doing a complete tour, even if its the best choice
            if score < smallestScore and (trailTuple[0] != self.StartingFoodSource and trailTuple[1] != self.StartingFoodSource):
                smallestScore = score
                nextFoodSource = self.Environment.FoodSourceDict[trailTuple[0]]

        return nextFoodSource

    def heuristic(self, distance, pheromoneScore):
        #TODO Improve this
        #Pheromone's reduce perceived distance, shorter is better
        return distance - pheromoneScore

    def get_ant_trail_total_length(self):
        totalTrailLength = 0
        sortedVisitedFoodSources = sorted(self.VisitedFoodSources, key=self.VisitedFoodSources.get)
        previous = sortedVisitedFoodSources[-1]
        for foodSource in sortedVisitedFoodSources:
            totalTrailLength += math.sqrt((foodSource.XPos - previous.XPos) ** 2 + (foodSource.YPos - previous.YPos) ** 2)
            previous = foodSource
        #Cache this value?
        return totalTrailLength
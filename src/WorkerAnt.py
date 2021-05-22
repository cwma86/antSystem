import math
import random

class WorkerAnt: 
    def __init__(self, environment):
        startingSpot = environment.FoodSources[random.randrange(0, len(environment.FoodSources))]
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = [startingSpot]
        self.Environment = environment

    def move(self):
        nextFoodSource = self.find_nearest_foodsource()

        if nextFoodSource is None:
            self.CurrentFoodSource = None
            return None

        #Sort tyuple by food source index
        if(self.CurrentFoodSource[0] < nextFoodSource[0]):
            pheromoneTrail = (self.CurrentFoodSource, nextFoodSource)
        else:
            pheromoneTrail = (nextFoodSource, self.CurrentFoodSource)

        self.CurrentFoodSource = nextFoodSource
        self.VisitedFoodSources.append(nextFoodSource)

        return pheromoneTrail

    def find_nearest_foodsource(self):
        nearestDistance = 0
        nearestFoodSource = None
        for foodSource in self.Environment.FoodSources:
            #Visit only new sources
            if foodSource in self.VisitedFoodSources or self.CurrentFoodSource[0] == foodSource[0]:
                continue

            #Keep track of the nearest food source
            distance = math.dist((self.CurrentFoodSource[1], self.CurrentFoodSource[2]), (foodSource[1], foodSource[2]))
            if nearestFoodSource is None or distance < nearestDistance:
                nearestFoodSource = foodSource
                nearestDistance = distance
        return nearestFoodSource

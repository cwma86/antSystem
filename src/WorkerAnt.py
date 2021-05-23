import math
import random

from FoodSource import Trail

class WorkerAnt: 
    def __init__(self, environment):
        startingSpot = environment.FoodSources[random.randrange(0, len(environment.FoodSources))]
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = set()
        self.VisitedFoodSources.add(startingSpot)
        self.Environment = environment

    def move(self):
        nextFoodSource = self.find_nearest_foodsource()

        if nextFoodSource is None:
            self.CurrentFoodSource = None
            return None

        pheromoneTrail = Trail(self.CurrentFoodSource, nextFoodSource)

        self.CurrentFoodSource = nextFoodSource
        self.VisitedFoodSources.add(nextFoodSource)

        return pheromoneTrail

    def find_nearest_foodsource(self):
        nearestDistance = 0
        nearestFoodSource = None
        for foodSource in self.Environment.FoodSources:
            #Visit only new sources
            if foodSource in self.VisitedFoodSources:
                continue
            if foodSource[0] == self.CurrentFoodSource[0]:
                continue

            #Keep track of the nearest food source
            distance = math.dist((self.CurrentFoodSource.XPos, self.CurrentFoodSource.YPos), (foodSource.XPos, foodSource.YPos))
            if nearestFoodSource is None or distance < nearestDistance:
                nearestFoodSource = foodSource
                nearestDistance = distance
        return nearestFoodSource

import math
from queue import PriorityQueue
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
        nearestFoodSource = None

        # Build the trail map from this food source if it does not exist.
        if self.CurrentFoodSource not in self.Environment.FoodSourceDistances:
            self.Environment.FoodSourceDistances[self.CurrentFoodSource] = list()
            distanceQueue = PriorityQueue()
            for foodSource in self.Environment.FoodSources:
                if foodSource != self.CurrentFoodSource:
                    distanceQueue.put(Trail(self.CurrentFoodSource, foodSource))

            while not distanceQueue.empty():
                self.Environment.FoodSourceDistances[self.CurrentFoodSource].append(distanceQueue.get())

            print(len(self.Environment.FoodSourceDistances))

        # Find the nearest unvisited food source
        trailDistanceList = self.Environment.FoodSourceDistances[self.CurrentFoodSource]
        for trail in trailDistanceList:
            targetFoodSource = trail.get_target_foodsource(self.CurrentFoodSource)
            if targetFoodSource not in self.VisitedFoodSources:
                nearestFoodSource = targetFoodSource
                break
            
        return nearestFoodSource

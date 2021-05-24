import random
import math

class WorkerAnt: 
    def __init__(self, environment):
        startingSpot = environment.FoodSources[random.randrange(0, len(environment.FoodSources))]
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = dict()  # FoodSource > visited order
        self.VisitedFoodSources[startingSpot] = 0
        self.Environment = environment
        self.ShuffledFoodSource = [i for i in environment.FoodSources]
        random.shuffle(self.ShuffledFoodSource)
        self.ShuffleCountdown = 5

    def move(self):
        trailTuple = self.find_nearest_foodsource()

        if trailTuple is None:
            self.CurrentFoodSource = None
            return None

        targetFoodSourceId = self.get_target_foodsource(self.CurrentFoodSource, trailTuple)
        targetFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]

        self.CurrentFoodSource = targetFoodSource
        self.VisitedFoodSources[targetFoodSource] = len(self.VisitedFoodSources)

        return trailTuple

    def find_nearest_foodsource(self):
        nearestFoodSourceTrailTuple = None

        # Build the trail map from this food source if it does not exist.
        if self.CurrentFoodSource not in self.Environment.FoodSourceDistances:
            trailList = list()

            if self.ShuffleCountdown == 0:
                random.shuffle(self.ShuffledFoodSource)
                self.ShuffleCountdown = 5

            self.ShuffleCountdown -= 1

            for foodSource in self.ShuffledFoodSource[0:100]:
                if foodSource != self.CurrentFoodSource:
                    distanceSquared = (foodSource.XPos - self.CurrentFoodSource.XPos) ** 2 + (foodSource.YPos - self.CurrentFoodSource.YPos) ** 2
                    trail = (foodSource.FoodSourceId, self.CurrentFoodSource.FoodSourceId, distanceSquared)
                    trailList.append(trail)

            trailList.sort(key= lambda t: t[2])
            self.Environment.FoodSourceDistances[self.CurrentFoodSource] = trailList

            # print(len(self.Environment.FoodSourceDistances))

        # Find the nearest unvisited food source
        trailDistanceList = self.Environment.FoodSourceDistances[self.CurrentFoodSource]
        for trail in trailDistanceList:
            targetFoodSourceId = self.get_target_foodsource(self.CurrentFoodSource, trail)
            targetFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]
            if targetFoodSource not in self.VisitedFoodSources:
                nearestFoodSourceTrailTuple = trail
                break

        return nearestFoodSourceTrailTuple

    def get_target_foodsource(self, currentFoodSource, trail):
        if currentFoodSource.FoodSourceId == trail[0]:
            return trail[1]
        elif currentFoodSource.FoodSourceId == trail[1]:
            return trail[0]

        return None

    def get_ant_trail_total_length(self):
        totalTrailLength = 0
        sortedVisitedFoodSources = sorted(self.VisitedFoodSources, key=self.VisitedFoodSources.get)
        previous = sortedVisitedFoodSources[-1]
        for foodSource in sortedVisitedFoodSources:
            totalTrailLength += math.sqrt((foodSource.XPos - previous.XPos) ** 2 + (foodSource.YPos - previous.YPos) ** 2)
            previous = foodSource
        #Cache this value?
        return totalTrailLength

import random

class WorkerAnt: 
    def __init__(self, environment):
        startingSpot = environment.FoodSources[random.randrange(0, len(environment.FoodSources))]
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = set()
        self.VisitedFoodSources.add(startingSpot)
        self.Environment = environment
        self.ShuffledFoodSource = [i for i in environment.FoodSources]
        random.shuffle(self.ShuffledFoodSource)
        self.ShuffleCountdown = 5

    def move(self):
        nextFoodSource = self.find_nearest_foodsource()

        if nextFoodSource is None:
            self.CurrentFoodSource = None
            return None

        targetFoodSourceId = self.get_target_foodsource(self.CurrentFoodSource, nextFoodSource)
        targetFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]

        self.CurrentFoodSource = targetFoodSource
        self.VisitedFoodSources.add(targetFoodSource)

        return nextFoodSource

    def find_nearest_foodsource(self):
        nearestFoodSource = None

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

            print(len(self.Environment.FoodSourceDistances))

        # Find the nearest unvisited food source
        trailDistanceList = self.Environment.FoodSourceDistances[self.CurrentFoodSource]
        for trail in trailDistanceList:
            targetFoodSourceId = self.get_target_foodsource(self.CurrentFoodSource, trail)
            targetFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]
            if targetFoodSource not in self.VisitedFoodSources:
                nearestFoodSource = trail
                break

        return nearestFoodSource

    def get_target_foodsource(self, currentFoodSource, trail):
        if currentFoodSource.FoodSourceId == trail[0]:
            return trail[1]
        elif currentFoodSource.FoodSourceId == trail[1]:
            return trail[0]

        return None
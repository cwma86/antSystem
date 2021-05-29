import random
import math

class WorkerAnt: 
    def __init__(self, environment):
        startingSpot = environment.FoodSources[random.randrange(0, len(environment.FoodSources))]
        self.CurrentFoodSource = startingSpot
        self.VisitedFoodSources = dict()  # FoodSource > visited order
        self.VisitedFoodSources[startingSpot] = 0
        self.Environment = environment
        self.ShuffledFoodSources = [i for i in environment.FoodSources]
        random.shuffle(self.ShuffledFoodSources)
        self.ShuffleCountdown = 5

    def move(self):
        trailTuple = self.find_nearest_foodsource()

        if trailTuple is None:
            self.CurrentFoodSource = None
            return None

        targetFoodSourceId = self.Environment.get_target_foodsource(self.CurrentFoodSource, trailTuple)
        targetFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]

        self.CurrentFoodSource = targetFoodSource

        #Keep track of the order of the visited Food Sources as we add them
        self.VisitedFoodSources[targetFoodSource] = len(self.VisitedFoodSources)

        return trailTuple

    def find_nearest_foodsource(self):
        nearestFoodSourceTrailTuple = None

        # Build the trail map from this food source if it does not exist.
        if self.CurrentFoodSource not in self.Environment.FoodSourceDistances:
            trailList = list()

            # Shuffle the Food Source list every 5 Worker Ant steps for variance.
            # We need to do this since we only generate distance trails from
            # the current food source for a fraction of the Food Sources in
            # the environment.
            # if self.ShuffleCountdown == 0:
            #     random.shuffle(self.ShuffledFoodSource)
            #     self.ShuffleCountdown = 5

            # self.ShuffleCountdown -= 1

            # random.shuffle(self.ShuffledFoodSources)
            # randomFoodSources = self.ShuffledFoodSources[0:len(self.Environment.FoodSources) // 5]
            randomFoodSources = self.ShuffledFoodSources

            for foodSource in randomFoodSources:
                if foodSource != self.CurrentFoodSource:
                    distanceSquared = (foodSource.XPos - self.CurrentFoodSource.XPos) ** 2 + (foodSource.YPos - self.CurrentFoodSource.YPos) ** 2
                    
                    # Sort the Food Sources by ID in the Tuple so that a path in either
                    # direction is the same trail. Otherwise A -> B would be a different
                    # trail than B -> A.
                    if foodSource.FoodSourceId < self.CurrentFoodSource.FoodSourceId:
                        trail = (foodSource.FoodSourceId, self.CurrentFoodSource.FoodSourceId, distanceSquared)
                    else:
                        trail = (self.CurrentFoodSource.FoodSourceId, foodSource.FoodSourceId, distanceSquared)

                    # Insert the trail into the trail distance dictionary for fast lookup
                    if trail[0] not in self.Environment.FoodSourceDistanceLookup:
                        self.Environment.FoodSourceDistanceLookup[trail[0]] = dict()
                    if trail[1] not in self.Environment.FoodSourceDistanceLookup[trail[0]]:
                        self.Environment.FoodSourceDistanceLookup[trail[0]][trail[1]] = trail[2]

                    # Insert the trail in to the trail distance list for sorting by distance
                    trailList.append(trail)

            # Sort the trail by distance, ascending
            trailList.sort(key= lambda t: t[2])

            # Store all the possible trails from this Food Source 
            # sorted by distance into a dictionary for later use.
            # This way distances between any two food sources will 
            # need to be calculated only one time for the entire run.
            self.Environment.FoodSourceDistances[self.CurrentFoodSource] = trailList

        # Find the nearest unvisited food source
        trailDistanceList = self.Environment.FoodSourceDistances[self.CurrentFoodSource]
        for trail in trailDistanceList:
            targetFoodSourceId = self.Environment.get_target_foodsource(self.CurrentFoodSource, trail)
            targetFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]
            if targetFoodSource not in self.VisitedFoodSources:
                nearestFoodSourceTrailTuple = trail
                break

        return nearestFoodSourceTrailTuple

    def get_ant_trail_total_length(self):
        totalTrailLength = 0
        sortedVisitedFoodSources = sorted(self.VisitedFoodSources, key=self.VisitedFoodSources.get)
        previous = sortedVisitedFoodSources[-1]
        for foodSource in sortedVisitedFoodSources:
            totalTrailLength += math.sqrt((foodSource.XPos - previous.XPos) ** 2 + (foodSource.YPos - previous.YPos) ** 2)
            previous = foodSource
        #Cache this value?
        return totalTrailLength

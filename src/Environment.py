import logging
from math import log
from WorkerAnt import WorkerAnt

class Environment:
    
    def __init__(self, foodSources, workerAntCount = None):
        self.FoodSources = foodSources
        self.FoodSourceDict = {f.FoodSourceId : f for f in self.FoodSources}
        self.PheromoneTrails = dict() #{ Tuple(foodSourceId, FoodSourceId): pheromoneScore }

        # Set the Worker Ant count or the default of the
        # (Food Source size divided by 20) or 5, whichever is greater.
        if workerAntCount == None:
            self.WorkerAntCount = max(len(self.FoodSources) // 20, 5)
        else:
            self.WorkerAntCount = workerAntCount

        # Trail distance dictionary for fast distance lookup
        self.FoodSourceDistanceLookup = dict() # {FoodSourceId: {FoodSourceId: distanceSquared}}

        # Trail distance list for closest distance lookup.
        self.FoodSourceDistances = dict() #{FoodSource: list of Tuple(foodSourceId, FoodSourceId, distanceSquared)}
        self.bestAnt = None

    def explore(self):
        ants = [WorkerAnt(self) for i in range(self.WorkerAntCount)]
        return self.__runWorkerAnts(ants) #PheromoneTrails


    def __runWorkerAnts(self, ants):
        shortest = float('inf')
        for ant in ants:
            while ant.CurrentFoodSource is not None:
                trail = ant.move()
                
                if trail is not None:
                    self.mark_trail(trail)
            length = ant.get_ant_trail_total_length()
            if (length < shortest):
                shortest = length
                self.bestAnt = ant
        print("Ant Shortest Trail Length", shortest)

        return self.PheromoneTrails

    def mark_trail(self, pheromoneTrail):
        # We just want the two food sources. Strip anything else.
        trailTuple = (pheromoneTrail[0], pheromoneTrail[1])

        self.PheromoneTrails[trailTuple] = self.PheromoneTrails[trailTuple] + 1

    # Since the Food Sources in the Trail Tuples are sorted by ID to make
    # A -> B and B -> A the same trail, we need this method to determine
    # which Food Source we are traveling to.
    def get_target_foodsourceId(self, currentFoodSource, trailTuple):
        if currentFoodSource.FoodSourceId == trailTuple[0]:
            return trailTuple[1]
        elif currentFoodSource.FoodSourceId == trailTuple[1]:
            return trailTuple[0]

        return None

    def get_pheromone_score(self, foodSourceId1, foodSourceId2):
        trailTuple = None
        if foodSourceId1 < foodSourceId2:
            trailTuple = (foodSourceId1, foodSourceId2)
        else:
            trailTuple = (foodSourceId2, foodSourceId1)

        return self.PheromoneTrails[trailTuple]

    def find_trail_distance(self, foodSourceId1, foodSourceId2):
        if foodSourceId1 < foodSourceId2:
            return self.FoodSourceDistanceLookup[foodSourceId1][foodSourceId2]
        else:
            return self.FoodSourceDistanceLookup[foodSourceId2][foodSourceId1]

from WorkerAnt import WorkerAnt
from MetricsTracker import MetricsTracker

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

        self.FoodSourceDistances = dict() #{FoodSource: list of Tuple(foodSourceId, FoodSourceId, distanceSquared)}
        self.MetricsTracker = MetricsTracker()
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

        # The food sources were already sorted by ID when they were generated in
        # the WorkerAnt find_nearest_foodsource() method
        # 
        # We are stripping the distance from the original tuple
        # both because we don't need it here, and also so the PheromoneTrails
        # dictionary is searchable. Including the distance in the key of
        # the dictionary would make finding a specific pheromone trail tough.
        trailTuple = (pheromoneTrail[0], pheromoneTrail[1])

        if trailTuple not in self.PheromoneTrails:
            self.PheromoneTrails[trailTuple] = 0

        self.PheromoneTrails[trailTuple] = self.PheromoneTrails[trailTuple] + 1

    # Since the Food Sources in the Trail Tuples are sorted by ID to make
    # A -> B and B -> A the same trail, we need this method to determine
    # which Food Source we are traveling to.
    def get_target_foodsource(self, currentFoodSource, trailTuple):
        if currentFoodSource.FoodSourceId == trailTuple[0]:
            return trailTuple[1]
        elif currentFoodSource.FoodSourceId == trailTuple[1]:
            return trailTuple[0]

        return None


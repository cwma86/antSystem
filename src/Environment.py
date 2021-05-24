from WorkerAnt import WorkerAnt
from MetricsTracker import MetricsTracker

class Environment:
    
    def __init__(self, foodSources, workerAntCount = None):
        self.FoodSources = foodSources
        self.FoodSourceDict = {f.FoodSourceId : f for f in self.FoodSources}
        self.PheromoneTrails = dict() #{ Tuple(foodSourceId, FoodSourceId, distanceSquared): pheromoneScore }

        # Set the Worker Ant count or the default of the
        # (Food Source size divided by 20) or 5, whichever is greater.
        if workerAntCount == None:
            self.WorkerAntCount = max(len(self.FoodSources) // 20, 5)
        else:
            self.WorkerAntCount = workerAntCount

        self.FoodSourceDistances = dict() #{FoodSource: list<Trail>}
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
        if pheromoneTrail not in self.PheromoneTrails:
            self.PheromoneTrails[pheromoneTrail] = 0

        self.PheromoneTrails[pheromoneTrail] = self.PheromoneTrails[pheromoneTrail] + 1


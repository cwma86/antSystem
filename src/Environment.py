from WorkerAnt import WorkerAnt

class Environment:
    def __init__(self, foodSources, workerAntCount = None):
        self.FoodSources = foodSources
        self.PheromoneTrails = dict() #{ (vertex, vertex): pheromoneScore }

        # Set the Worker Ant count or the default of the
        # (Food Source size divided by 20) or 5, whichever is greater.
        if workerAntCount == None:
            self.WorkerAntCount = max(len(self.FoodSources) // 20, 5)
        else:
            self.WorkerAntCount = workerAntCount

    def explore(self):
        ants = [WorkerAnt(self) for i in range(self.WorkerAntCount)]
        return self.__runWorkerAnts(ants) #PheromoneTrails


    def __runWorkerAnts(self, ants):    
        for ant in ants:
            while ant.CurrentFoodSource is not None:
                trail = ant.move()
                
                if trail is not None:
                    self.mark_trail(trail)

        return self.PheromoneTrails
        
    def mark_trail(self, pheromoneTrail):
        if pheromoneTrail not in self.PheromoneTrails:
            self.PheromoneTrails[pheromoneTrail] = 0

        self.PheromoneTrails[pheromoneTrail] = self.PheromoneTrails[pheromoneTrail] + 1


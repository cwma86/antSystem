from WorkerAnt import WorkerAnt

class Environment:
    def __init__(self, foodSources):
        self.FoodSources = foodSources
        self.PheromoneTrails = dict() #{ (vertex, vertex): pheromoneScore }

    def explore(self):
        ants = [WorkerAnt(self) for i in range(len(self.FoodSources) // 10)]
        
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


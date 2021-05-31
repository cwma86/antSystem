import logging
from math import log
from WorkerAnt import WorkerAnt

class Environment:
    
    def __init__(self, foodSources, workerAntCount = None):

        # The original Food Source list
        self.FoodSources = foodSources

        # The quick Food Source lookup dictionary
        self.FoodSourceDict = dict() # { FoodSourceId: FoodSource }

        # The pheromone trails and the strengths
        self.PheromoneTrails = dict() #{ Tuple(foodSourceId, FoodSourceId): pheromoneScore }

        # Trail distance dictionary for fast distance lookup
        self.FoodSourceDistanceLookup = dict() # {FoodSourceId: {FoodSourceId: distanceSquared}}

        # Trail distance list for closest distance lookup.
        self.FoodSourceDistances = dict() #{FoodSourceId: list of Tuple(foodSourceId, FoodSourceId, distanceSquared)}

        self.__prepare_lookup_dictionaries()

        # Set the Worker Ant count or the default of the
        # (Food Source size divided by 20) or 5, whichever is greater.
        if workerAntCount == None:
            self.WorkerAntCount = max(len(self.FoodSources) // 20, 5)
        else:
            self.WorkerAntCount = workerAntCount
        
        self.bestAnt = None

    def explore(self):
        ants = [WorkerAnt(self) for i in range(self.WorkerAntCount)]
        return self.__runWorkerAnts(ants) #PheromoneTrails


    def __runWorkerAnts(self, ants):
        shortest = float('inf')

        logging.info("The Worker Ants are now laying Pheromone Trails")
        for ant in ants:
            while ant.CurrentFoodSource is not None:
                trail = ant.move()
                
                if trail is not None:
                    self.__mark_trail(trail)

            length = ant.get_ant_trail_total_length()
            if (length < shortest):
                shortest = length
                self.bestAnt = ant
        logging.info(f"Ant Shortest Trail Length: {shortest}")

        # Validate Food Source Distances
        for foodSource in self.FoodSources:
            if foodSource.FoodSourceId not in self.FoodSourceDistances:
                logging.error(f'Food Source ID {foodSource.FoodSourceId} not present in the distance list')

        logging.info(f'Non-zero Pheromone Trails: {len([i for i in self.PheromoneTrails if self.PheromoneTrails[i] != 0])}')
        logging.info(f'Zero Pheromone Trails: {len([i for i in self.PheromoneTrails if self.PheromoneTrails[i] == 0])}')

        return self.PheromoneTrails

    def __mark_trail(self, pheromoneTrail):
        # We just want the two food sources. Strip anything else.
        trailTuple = (pheromoneTrail[0], pheromoneTrail[1])

        if pheromoneTrail[1] < pheromoneTrail[0]:
            logging.error('A Pheromone Trail is switched')

        if pheromoneTrail[1] == pheromoneTrail[0]:
            logging.error('Invalid matched Pheromone Trail')

        self.PheromoneTrails[trailTuple] = self.PheromoneTrails[trailTuple] + 1

    # Since the Food Sources in the Trail Tuples are sorted by ID to make
    # A -> B and B -> A the same trail, we need this method to determine
    # which Food Source we are traveling to.
    def get_target_foodsourceId(self, currentFoodSourceId, trailTuple):
        if currentFoodSourceId == trailTuple[0]:
            return trailTuple[1]
        elif currentFoodSourceId == trailTuple[1]:
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

    def __prepare_lookup_dictionaries(self):
        # Organize the food sources into a quick lookup dictionary
        self.FoodSourceDict = {f.FoodSourceId : f for f in self.FoodSources}

        # Store the distances between all food sources in a quick lookup dictionary
        logging.info("Food Source Lookup Generation Begin")
        for i in range(len(self.FoodSources) - 1):
            for j in range(i + 1, len(self.FoodSources)):
                foodSource1 = self.FoodSources[i]
                foodSource2 = self.FoodSources[j]
                distanceSquared = (foodSource1.XPos - foodSource2.XPos) ** 2 + (foodSource1.YPos - foodSource2.YPos) ** 2

                if foodSource1.FoodSourceId not in self.FoodSourceDistanceLookup:
                    self.FoodSourceDistanceLookup[foodSource1.FoodSourceId] = dict()
                self.FoodSourceDistanceLookup[foodSource1.FoodSourceId][foodSource2.FoodSourceId] = distanceSquared
        logging.info("Food Source Lookup Generation End")

        # Store all trails and their distance from each food source
        logging.info("Trail Distance Tuple Generation Begin")
        for foodSource1 in self.FoodSources:
            if foodSource1.FoodSourceId not in self.FoodSourceDistances:
                self.FoodSourceDistances[foodSource1.FoodSourceId] = list()

            for foodSource2 in self.FoodSources:
                if foodSource1 == foodSource2:
                    continue
                
                # Ensure the proper ascending order of the Food Source Id
                foodSourceId1 = None
                foodSourceId2 = None
                if foodSource1.FoodSourceId < foodSource2.FoodSourceId:
                    foodSourceId1 = foodSource1.FoodSourceId
                    foodSourceId2 = foodSource2.FoodSourceId
                else:
                    foodSourceId1 = foodSource2.FoodSourceId
                    foodSourceId2 = foodSource1.FoodSourceId

                distanceSquared = self.FoodSourceDistanceLookup[foodSourceId1][foodSourceId2]

                trailDistanceTuple = (foodSourceId1, foodSourceId2, distanceSquared)
                self.FoodSourceDistances[foodSource1.FoodSourceId].append(trailDistanceTuple)
        logging.info("Trail Distance Tuple Generation End")

        # Sort all the distance tuples by distance ascending
        logging.info("Sort Trail Distance Begin")
        for foodSourceId in self.FoodSourceDistances:
            self.FoodSourceDistances[foodSourceId].sort(key= lambda t: t[2])
        logging.info("Sort Trail Distance End")

        # Initialize the Pheromone Trail strength dictionary
        logging.info("Pheromone Trail initialization Begin")
        for i in range(len(self.FoodSources) - 1):
            for j in range(i + 1, len(self.FoodSources)):
                foodSource1 = self.FoodSources[i]
                foodSource2 = self.FoodSources[j]

                trailTuple = (foodSource1.FoodSourceId, foodSource2.FoodSourceId)

                self.PheromoneTrails[trailTuple] = 0
        logging.info("Pheromone Trail initialization End")
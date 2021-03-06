import logging
import numpy
import math

from WorkerAnt import WorkerAnt

class Environment:
    
    def __init__(self, foodSources, workerAntCount = None):

        # The original Food Source list
        self.FoodSources = foodSources

        # The quick Food Source lookup dictionary
        self.FoodSourceDict = dict() # { FoodSourceId: FoodSource }

        # The pheromone trails and the strengths
        self.PheromoneTrails = dict() # { FoodSourceId: { FoodSourceId: pheromoneScore } }

        # The possible Pheromone Trails for each Food Source, sorted by strongest Pheromone Score descending
        self.PheromoneTrailsBestLookup = dict() # { FoodSourceId: list of Tuple(foodSourceId, pheromoneScore) }

        # Trail distance dictionary for fast distance lookup
        self.FoodSourceDistanceLookup = dict() # { FoodSourceId: { FoodSourceId: distance } }

        # The possible paths to take for each Food Source, sorted by distance descending
        self.FoodSourceDistances = dict() # { FoodSourceId: list of Tuple(foodSourceId, FoodSourceId, distance) }

        # The standard deviations are used to determine whether to take the strongest pheromone
        # trail or the trail to the closest food source
        self.DistanceAverage = 0
        self.DistanceStDev = 0
        self.PheromoneScoreAverage = 0
        self.PheromoneScoreStDev = 0

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

        logging.debug("The Worker Ants are now laying Pheromone Trails...")
        for ant in ants:
            while ant.CurrentFoodSource is not None:
                trail = ant.move()
                
                if trail is not None:
                    self.__mark_trail(trail)

            length = ant.get_ant_trail_total_length()
            if (length < shortest):
                shortest = length
                self.bestAnt = ant
        logging.debug(f"Ant Shortest Trail Length: {shortest}")

        # Validate Food Source Distances
        for foodSource in self.FoodSources:
            if foodSource.FoodSourceId not in self.FoodSourceDistances:
                logging.error(f'Food Source ID {foodSource.FoodSourceId} not present in the distance list')

        logging.debug(f'Non-zero Pheromone Trails: {sum([len([i for i in d if d[i] != 0]) for d in [self.PheromoneTrails[i] for i in self.PheromoneTrails]])}')
        logging.debug(f'Zero Pheromone Trails: {sum([len([i for i in d if d[i] == 0]) for d in [self.PheromoneTrails[i] for i in self.PheromoneTrails]])}')

        # Store all the pheromone trails as sortable lists for each food source
        logging.debug("Generating dictionary of sorted pheromone trails for each food source...")
        for foodSource1 in self.FoodSources:
            if foodSource1.FoodSourceId not in self.PheromoneTrailsBestLookup:
                self.PheromoneTrailsBestLookup[foodSource1.FoodSourceId] = list()

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

                pheromoneScore = self.PheromoneTrails[foodSourceId1][foodSourceId2]

                if pheromoneScore > 0:
                    pheromoneScoreTuple = (foodSource2.FoodSourceId, pheromoneScore)
                    self.PheromoneTrailsBestLookup[foodSource1.FoodSourceId].append(pheromoneScoreTuple)
        logging.debug("Generating dictionary of sorted pheromone trails End")

        # Sort all the pheromone tuples by score descending
        logging.debug("Sort Best Pheromone Trails Begin...")
        for foodSourceId in self.PheromoneTrailsBestLookup:
            self.PheromoneTrailsBestLookup[foodSourceId].sort(key= lambda t: t[1])
            self.PheromoneTrailsBestLookup[foodSourceId].reverse()
        logging.debug("Sort Best Pheromone Trails End")

        pheromoneScores = numpy.array([])
        for foodSourceId in self.PheromoneTrailsBestLookup:
            pheromones = [i[1] for i in self.PheromoneTrailsBestLookup[foodSourceId] if i[1] > 0]
            if len(pheromones) > 0:
                pheromoneScores = numpy.append(pheromoneScores, pheromones)
        self.PheromoneScoreAverage = pheromoneScores.sum() / len(pheromoneScores)
        self.PheromoneScoreStDev = pheromoneScores.std()
        logging.debug(f'Pheromone Score Average: {self.PheromoneScoreAverage}')
        logging.debug(f'Pheromone Score STD: {self.PheromoneScoreStDev}')

        return self.PheromoneTrails

    def __mark_trail(self, pheromoneTrail):
        # We just want the two food sources. Strip anything else.
        trailTuple = (pheromoneTrail[0], pheromoneTrail[1])

        if pheromoneTrail[1] < pheromoneTrail[0]:
            logging.error('A Pheromone Trail is switched')

        if pheromoneTrail[1] == pheromoneTrail[0]:
            logging.error('Invalid matched Pheromone Trail')

        self.PheromoneTrails[pheromoneTrail[0]][pheromoneTrail[1]] = self.PheromoneTrails[pheromoneTrail[0]][pheromoneTrail[1]] + 1

    def score_tour(self, tour):
        totalLength = 0

        if(len(tour) != len(self.FoodSources)):
            logging.error('TOUR NOT COMPLETE')
            logging.error(f'TOUR SIZE: {len(tour)}')

        for i in range(len(tour) - 1):
            totalLength += self.find_trail_distance(tour[i], tour[i + 1])

        totalLength += self.find_trail_distance(tour[0], tour[len(tour) - 1])
        
        return totalLength

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
        if foodSourceId1 < foodSourceId2:
            return self.PheromoneTrails[foodSourceId1][foodSourceId2]
        else:
            return self.PheromoneTrails[foodSourceId2][foodSourceId1]

    def find_trail_distance(self, foodSourceId1, foodSourceId2):
        if foodSourceId1 < foodSourceId2:
            return self.FoodSourceDistanceLookup[foodSourceId1][foodSourceId2]
        else:
            return self.FoodSourceDistanceLookup[foodSourceId2][foodSourceId1]

    def find_best_pheromone_trails(self, foodSourceId):
        pheromoneList = self.PheromoneTrailsBestLookup[foodSourceId]
        return pheromoneList

    def find_closest_distances(self, foodSourceId):
        return self.FoodSourceDistances[foodSourceId]

    def __prepare_lookup_dictionaries(self):
        # Organize the food sources into a quick lookup dictionary
        self.FoodSourceDict = {f.FoodSourceId : f for f in self.FoodSources}

        # Store the distances between all food sources in a quick lookup dictionary
        logging.debug("Food Source Distance Lookup Generation Begin...")
        for i in range(len(self.FoodSources) - 1):
            foodSource1 = self.FoodSources[i]
            for j in range(i + 1, len(self.FoodSources)):
                
                foodSource2 = self.FoodSources[j]
                distance = math.sqrt((foodSource1.XPos - foodSource2.XPos) ** 2 + (foodSource1.YPos - foodSource2.YPos) ** 2)

                if foodSource1.FoodSourceId not in self.FoodSourceDistanceLookup:
                    self.FoodSourceDistanceLookup[foodSource1.FoodSourceId] = dict()
                self.FoodSourceDistanceLookup[foodSource1.FoodSourceId][foodSource2.FoodSourceId] = distance
        logging.debug("Food Source Distance Lookup Generation End")

        # Store all trails and their distance from each food source
        logging.debug("Trail Distance Tuple Generation Begin...")
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

                distance = self.FoodSourceDistanceLookup[foodSourceId1][foodSourceId2]

                trailDistanceTuple = (foodSourceId1, foodSourceId2, distance)
                self.FoodSourceDistances[foodSource1.FoodSourceId].append(trailDistanceTuple)
        logging.debug("Trail Distance Tuple Generation End")

        # Sort all the distance tuples by distance ascending
        logging.debug("Sort Trail Distance Begin...")
        for foodSourceId in self.FoodSourceDistances:
            self.FoodSourceDistances[foodSourceId].sort(key= lambda t: t[2])
        logging.debug("Sort Trail Distance End")

        # Initialize the Pheromone Trail strength dictionary
        logging.debug("Pheromone Trail initialization Begin...")
        for i in range(len(self.FoodSources) - 1):
            for j in range(i + 1, len(self.FoodSources)):
                foodSource1 = self.FoodSources[i]
                foodSource2 = self.FoodSources[j]

                if foodSource1.FoodSourceId not in self.PheromoneTrails:
                    self.PheromoneTrails[foodSource1.FoodSourceId] = dict()

                self.PheromoneTrails[foodSource1.FoodSourceId][foodSource2.FoodSourceId] = 0
        logging.debug("Pheromone Trail initialization End")

        distances = numpy.array([])
        for foodSourceId in self.FoodSourceDistances:
            distances = numpy.append(distances, [i[2] for i in self.FoodSourceDistances[foodSourceId]])
        logging.debug(f'Distances Values: {distances}')
        self.DistanceAverage = distances.sum() / len(distances)
        self.DistanceStDev = distances.std()
        logging.debug(f'Distance Average: {self.DistanceAverage}')
        logging.debug(f'Distance STD: {self.DistanceStDev}')
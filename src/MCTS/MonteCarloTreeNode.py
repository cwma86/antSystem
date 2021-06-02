import logging
import math
import random

class MCTSNode:
    def __init__(self, environment, parent, currentFoodSource, ongoingTour = list()):

        self.Environment = environment
        self.RunCount = 0
        self.AverageTrailLength = 0

        self.Parent = parent

        self.OngoingTour = list(ongoingTour)

        # Append the given food source to the tour.
        self.VisitedNodes = set(self.OngoingTour)

        if currentFoodSource not in self.VisitedNodes:
            self.OngoingTour.append(currentFoodSource.FoodSourceId)
            self.VisitedNodes.add(currentFoodSource)

        self.CurrentFoodSource = currentFoodSource
        self.ChildNodes = dict()
        self.ChildNodesVisited = set()
        
        self.PheromoneScore = 0
        if parent is not None:
            parentFoodSourceId = parent.get_foodsource().FoodSourceId
            self.PheromoneScore = environment.get_pheromone_score(parentFoodSourceId, currentFoodSource.FoodSourceId)

        self.BestTourDistance = math.inf
        self.BestRollout = None

        self.VisitCount = 0
        self.IsFullyExpanded = False
        self.IsTerminalNode = False

    def select(self):
        if self.IsTerminalNode:
            return self

        if self.IsFullyExpanded:
            bestChild = self.find_best_child()

            if bestChild is None:
                self.IsTerminalNode = True
                return self
            return bestChild.select()

        if len(self.ChildNodes) == 0:
            self.populate_children()

            if len(self.ChildNodes) == 0:
                self.IsTerminalNode = True

                return self

        unvisitedChild = self.pick_unvisited_child()

        if unvisitedChild is None:
            self.IsFullyExpanded = True
            return self
            
        return unvisitedChild

    def rollout(self):

        visitedNodes = set(self.OngoingTour)

        rolloutPaths = self.find_rollout_candidates(self.CurrentFoodSource.FoodSourceId, visitedNodes)

        if len(rolloutPaths) == 0:
            return (self.Environment.score_tour(list(self.OngoingTour)), list(self.OngoingTour))

        pathRolloutScores = []
        bestPathScore = math.inf
        bestPath = None

        for pathFoodSource in rolloutPaths:
            # Navigate unvisited food sources along the trails with the strongest Pheromones
            # until all Food Sources have been visited.
            rolloutTour = list(self.OngoingTour)

            # Track this node's visited food sources as we simulate the tour
            rolloutVisitedNodes = set(rolloutTour)

            # Find the strongest unvisited pheromone trail from this point
            currentFoodSource = self.CurrentFoodSource
            nextFoodSource = pathFoodSource

            while nextFoodSource is not None:
                rolloutTour.append(nextFoodSource.FoodSourceId)
                rolloutVisitedNodes.add(nextFoodSource.FoodSourceId)

                currentFoodSource = nextFoodSource

                nextFoodSource = self.find_foodsource_from_strongest_unvisited_pheromone_trail(currentFoodSource.FoodSourceId, rolloutVisitedNodes)

            tourScore = self.Environment.score_tour(rolloutTour)

            if tourScore < bestPathScore:
                bestPathScore = tourScore
                bestPath = rolloutTour

            pathRolloutScores.append(tourScore)

        return (bestPathScore, bestPath)

    def propagate(self, rolloutScore, rolloutPath):
        currentNode = self

        currentNode.BestTourDistance = rolloutScore
        currentNode.BestRollout = rolloutPath
        currentNode.VisitCount = 1

        if(currentNode.Parent is not None):
            currentNode.Parent.ChildNodesVisited.add(currentNode.get_foodsource().FoodSourceId)

        parent = currentNode.Parent
        while parent is not None:
            # propagate the best tour distance to the parent
            if currentNode.BestTourDistance < parent.BestTourDistance:
                parent.BestTourDistance = currentNode.BestTourDistance
                parent.BestRollout = currentNode.BestRollout
            
            # Increment the parent's visit count
            parent.VisitCount += 1

            # Move one step up the tree
            currentNode = parent
            parent = currentNode.Parent

    def find_foodsource_from_strongest_unvisited_pheromone_trail(self, currentFoodSourceId, visitedFoodSources):
        return self.__find_best_pheromone_or_closest_foodsource(currentFoodSourceId, visitedFoodSources)

    def pick_unvisited_child(self):
        bestUnvisitedFoodSource = self.__find_best_pheromone_or_closest_foodsource()

        if bestUnvisitedFoodSource is None:
            return None

        node = self.ChildNodes[bestUnvisitedFoodSource.FoodSourceId]
        return node

    def __find_best_pheromone_or_closest_foodsource(self, currentFoodSourceId = None, visitedFoodSources = None):
        if currentFoodSourceId is not None and visitedFoodSources is None:
            logging.error("Invalid data sent to the Next Node method")
            return TypeError()

        isRollout = True

        if currentFoodSourceId is None:
            isRollout = False
            currentFoodSourceId = self.CurrentFoodSource.FoodSourceId
            
            # Mark the children of this Node already rolled out by the MCTS as visited
            visitedFoodSources = set([childFoodSourceId for childFoodSourceId in self.ChildNodes if self.ChildNodes[childFoodSourceId].get_visit_count() != 0])
            
            # Include the food sources in the existing tour as visited.
            for tourStop in self.OngoingTour:
                visitedFoodSources.add(tourStop)

        # Pick the unvisited Food Source with the highest pheromone score
        bestPheromoneTargets = self.Environment.find_best_pheromone_trails(currentFoodSourceId)
        bestPheromoneFoodSource = None
        bestPheromoneFoodSourceId = None
        for bestPheromone in bestPheromoneTargets:
            foodSourceIdTarget = bestPheromone[0]
            if foodSourceIdTarget not in visitedFoodSources and (isRollout or foodSourceIdTarget in self.ChildNodes):
                bestPheromoneFoodSource = self.Environment.FoodSourceDict[foodSourceIdTarget]
                bestPheromoneFoodSourceId = foodSourceIdTarget
                break

        # If there are no available pheromone trails from this food source, pick the closest unvisited food source
        closestTargetTrailTuples = self.Environment.find_closest_distances(currentFoodSourceId)
        closestFoodSource = None
        closestFoodSourceId = None
        for closestTrail in closestTargetTrailTuples:
            targetFoodSourceId = self.Environment.get_target_foodsourceId(currentFoodSourceId, closestTrail)
            if targetFoodSourceId not in visitedFoodSources and (isRollout or targetFoodSourceId in self.ChildNodes):
                closestFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]
                closestFoodSourceId = targetFoodSourceId
                break

        # Determine whether to take the closest food source or the strongest
        # pheromone trail
        if bestPheromoneFoodSource is not None and closestFoodSource is None:
            return bestPheromoneFoodSource
        elif closestFoodSource is not None and bestPheromoneFoodSource is None:
            return closestFoodSource
        elif bestPheromoneFoodSource is not None and closestFoodSource is not None:
            pheromoneDeviation = (
                self.Environment.get_pheromone_score(currentFoodSourceId, bestPheromoneFoodSourceId)
                - self.Environment.PheromoneScoreAverage
            ) / self.Environment.PheromoneScoreStDev
            distanceDeviation = -(
                self.Environment.find_trail_distance(currentFoodSourceId, closestFoodSourceId)
                - self.Environment.DistanceAverage
            ) / self.Environment.DistanceStDev

            if pheromoneDeviation > distanceDeviation:
                return bestPheromoneFoodSource
            else:
                return closestFoodSource

    def find_rollout_candidates(self, currentFoodSourceId, visitedFoodSources):
        if currentFoodSourceId is not None and visitedFoodSources is None:
            logging.error("Invalid data sent to the Next Node method")
            return TypeError()

        rolloutCandidates = set()

        # Pick the unvisited Food Source with the highest pheromone score
        bestPheromoneTargets = self.Environment.find_best_pheromone_trails(currentFoodSourceId)
        pheromonePathCount = 0
        for bestPheromone in bestPheromoneTargets:
            if pheromonePathCount >= 10:
                break
            foodSourceIdTarget = bestPheromone[0]
            if foodSourceIdTarget not in visitedFoodSources:
                rolloutCandidates.add(foodSourceIdTarget)
                pheromonePathCount += 1

        # If there are no available pheromone trails from this food source, pick the closest unvisited food source
        closestTargetTrailTuples = self.Environment.find_closest_distances(currentFoodSourceId)
        closestPathCount = 0
        for closestTrail in closestTargetTrailTuples:
            if closestPathCount >= 10:
                break
            targetFoodSourceId = self.Environment.get_target_foodsourceId(currentFoodSourceId, closestTrail)
            if targetFoodSourceId not in visitedFoodSources:
                rolloutCandidates.add(targetFoodSourceId)
                closestPathCount += 1

        candidates = [(i, self.Environment.FoodSourceDict[i], (
                self.Environment.get_pheromone_score(currentFoodSourceId, i)
                - self.Environment.PheromoneScoreAverage
            ) / self.Environment.PheromoneScoreStDev,
            -(
                self.Environment.find_trail_distance(currentFoodSourceId, i)
                - self.Environment.DistanceAverage
            ) / self.Environment.DistanceStDev
        ) for i in rolloutCandidates]

        candidates.sort(key=lambda t: max(t[2],t[3]))

        return [i[1] for i in candidates][0:10]

    def fully_expanded(self):
        return len([i for i in self.ChildNodes.values() if i.get_visit_count() == 0])
        
    def find_best_child(self):
        bestChild = None
        bestChildScore = 0
        for child in self.ChildNodes.values():
            childScore = child.upper_confidence_bound()
            if childScore > bestChildScore:
                bestChild = child
                bestChildScore = childScore

        return bestChild

    def upper_confidence_bound(self):
        return (
            self.BestTourDistance / len(self.Environment.FoodSources)
            + self.Environment.DistanceAverage / 4 * math.sqrt(math.log(self.Parent.get_visit_count()) / self.VisitCount)
        )

    def populate_children(self):
        # Create Trails between the current Food Source
        # and all unvisited Food Sources

        bestPheromoneTrails = self.Environment.find_best_pheromone_trails(self.CurrentFoodSource.FoodSourceId)
        closestTrails = self.Environment.find_closest_distances(self.CurrentFoodSource.FoodSourceId)

        foodSourceIds = set()

        pheromoneNodeCount = 0
        for bestPheromoneTrail in bestPheromoneTrails:
            if pheromoneNodeCount >= 50:
                break
            foodSourceId = bestPheromoneTrail[0]
            if foodSourceId not in self.VisitedNodes:
                foodSourceIds.add(foodSourceId)
                pheromoneNodeCount += 1

        closestNodeCount = 0
        for closestTrail in closestTrails:
            if closestNodeCount >= 50:
                break
            closestFoodSourceId = self.Environment.get_target_foodsourceId(self.CurrentFoodSource.FoodSourceId, closestTrail)
            if closestFoodSourceId not in self.VisitedNodes:
                foodSourceIds.add(closestFoodSourceId)
                closestNodeCount += 1

        for foodSourceId in foodSourceIds:
            foodSource = self.Environment.FoodSourceDict[foodSourceId]
            node = MCTSNode(self.Environment, self, foodSource, self.OngoingTour)
            self.ChildNodes[foodSource.FoodSourceId] = node

    def simulate(self):
        pass

    def get_foodsource(self):
        return self.CurrentFoodSource

    def get_pheromone_score(self):
        return self.PheromoneScore

    def get_visit_count(self):
        return self.VisitCount
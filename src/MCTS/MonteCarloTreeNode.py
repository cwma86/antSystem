import logging
import math
import random

class MCTSNode:
    def __init__(self, environment, parent, currentFoodSource, ongoingTour = set()):

        self.Environment = environment
        self.RunCount = 0
        self.AverageTrailLength = 0

        self.Parent = parent

        self.OngoingTour = ongoingTour

        # Append the given food source to the tour.
        self.VisitedNodes = set(ongoingTour)
        self.VisitedNodes.add(currentFoodSource.FoodSourceId)

        self.CurrentFoodSource = currentFoodSource
        self.ChildNodes = dict()
        self.ChildNodesVisited = set()
        
        self.PheromoneScore = 0
        if parent is not None:
            parentFoodSourceId = parent.get_foodsource().FoodSourceId
            self.PheromoneScore = environment.get_pheromone_score(parentFoodSourceId, currentFoodSource.FoodSourceId)

        self.AverageTourDistance = math.inf
        self.BestTourDistance = math.inf
        self.VisitCount = 0
        self.IsFullyExpanded = False

    def select(self):
        if len(self.ChildNodes) == 0:
            logging.info(f'Node {self.CurrentFoodSource.FoodSourceId} is populating its children')
            self.populate_children()

        if not self.IsFullyExpanded:
            unvisitedChild = self.pick_unvisited_child()

            if unvisitedChild is not None:
                return unvisitedChild

            logging.info(f'Node {self.CurrentFoodSource.FoodSourceId} has no more unvisited children. Marking as Fully Expanded')

            # The only time we get here is when there are no more unvisited children
            # Mark this node as fully expanded and then select the best child
            self.IsFullyExpanded = True

        return self.find_best_child().select()

    def rollout(self):
        # Track this node's visited food sources as we simulate the tour
        rolloutVisitedNodes = set(self.VisitedNodes)

        # Navigate unvisited food sources along the trails with the strongest Pheromones
        # until all Food Sources have been visited.
        rolloutTour = list(self.VisitedNodes)

        # Find the strongest unvisited pheromone trail from this point
        currentFoodSourceId = self.CurrentFoodSource.FoodSourceId
        nextFoodSource = self.find_foodsource_from_strongest_unvisited_pheromone_trail(currentFoodSourceId, rolloutVisitedNodes)

        while nextFoodSource is not None:
            rolloutTour.append(nextFoodSource.FoodSourceId)
            rolloutVisitedNodes.add(nextFoodSource.FoodSourceId)

            currentFoodSource = nextFoodSource

            nextFoodSource = self.find_foodsource_from_strongest_unvisited_pheromone_trail(currentFoodSource.FoodSourceId, rolloutVisitedNodes)

        tourScore = self.score_tour(rolloutTour)

        return tourScore

    def propagate(self, rolloutScore):
        currentNode = self

        currentNode.BestTourDistance = rolloutScore
        currentNode.AverageTourDistance = rolloutScore
        currentNode.VisitCount = 1

        parent = currentNode.Parent
        while parent is not None:
            # propagate the best tour distance to the parent
            if currentNode.BestTourDistance < parent.BestTourDistance:
                parent.BestTourDistance = currentNode.BestTourDistance

            # Add the current node to the parent's visited nodes
            if currentNode not in parent.ChildNodesVisited:
                parent.ChildNodesVisited.add(currentNode)

            # Calculate the parent's new average tour distance
            summedChildScores = 0
            for visitedNode in parent.ChildNodesVisited:
                summedChildScores += visitedNode.AverageTourDistance

            parent.AverageTourDistance = summedChildScores / len(parent.ChildNodesVisited)
            
            # Increment the parent's visit count
            parent.VisitCount += 1

            # Move one step up the tree
            currentNode = parent
            parent = currentNode.Parent
    
    def score_tour(self, tour):
        totalLength = 0

        if(len(tour) != len(self.Environment.FoodSources)):
            logging.error('TOUR NOT COMPLETE')
            logging.error(f'TOUR SIZE: {len(tour)}')

        for i in range(len(tour) - 1):
            totalLength += math.sqrt(self.Environment.find_trail_distance(tour[i], tour[i + 1]))
        
        return totalLength

    def find_foodsource_from_strongest_unvisited_pheromone_trail(self, currentFoodSourceId, visitedFoodSources):
        return self.__find_best_pheromone_or_closest_foodsource(currentFoodSourceId, visitedFoodSources)

    def pick_unvisited_child(self):
        bestUnvisitedFoodSource = self.__find_best_pheromone_or_closest_foodsource()

        node = self.ChildNodes[bestUnvisitedFoodSource.FoodSourceId]

        return node

    def __find_best_pheromone_or_closest_foodsource(self, currentFoodSourceId = None, visitedFoodSources = None):
        if currentFoodSourceId is not None and visitedFoodSources is None:
            logging.error("Invalid data sent to the Next Node method")
            return TypeError()

        if currentFoodSourceId is None:
            currentFoodSourceId = self.CurrentFoodSource.FoodSourceId
            
            # Mark the children of this Node already rolled out by the MCTS as visited
            visitedFoodSources = set([foodSourceId for foodSourceId in self.ChildNodes if self.ChildNodes[foodSourceId].get_visit_count() != 0])
            
            # Include the food sources in the existing tour as visited.
            for tourStop in self.OngoingTour:
                visitedFoodSources.add(tourStop)


        # Pick the unvisited Food Source with the highest pheromone score
        bestPheromoneTargets = self.Environment.find_best_pheromone_trails(currentFoodSourceId)
        bestPheromoneFoodSource = None
        for bestPheromone in bestPheromoneTargets:
            foodSourceIdTarget = bestPheromone[0]
            if foodSourceIdTarget not in visitedFoodSources:
                bestPheromoneFoodSource = self.Environment.FoodSourceDict[foodSourceIdTarget]
                break

        # If there are no available pheromone trails from this food source, pick the closest unvisited food source
        if bestPheromoneFoodSource is None:
            closestTargetTrailTuples = self.Environment.find_closest_distances(currentFoodSourceId)
            for closestTrail in closestTargetTrailTuples:
                targetFoodSourceId = self.Environment.get_target_foodsourceId(currentFoodSourceId, closestTrail)
                if targetFoodSourceId not in visitedFoodSources:
                    bestPheromoneFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]
                    break

        # If there were no pheromone trails from this food source, log an error
        if bestPheromoneFoodSource is None:
            logging.error(f'Food Source ID: {currentFoodSourceId} has no available trails from this point.')

        return bestPheromoneFoodSource

    def fully_expanded(self):
        return len([i for i in self.ChildNodes.values() if i.get_visit_count() == 0])
        
    def find_best_child(self):
        bestChild = None
        bestChildScore = 0
        for child in self.ChildNodes:
            childScore = child.upper_confidence_bound()
            if childScore > bestChildScore:
                bestChild = child
                bestChildScore = childScore

        return bestChild

    def upper_confidence_bound(self):
        return (
            self.AverageTourDistance 
            + 1.41 * math.sqrt(math.log(self.Parent.get_visit_count()) / self.VisitCount)
        )

    def populate_children(self):
        # Create Trails between the current Food Source
        # and all unvisited Food Sources
        for foodSource in self.Environment.FoodSources:
            if foodSource.FoodSourceId not in self.VisitedNodes and foodSource != self.CurrentFoodSource:
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
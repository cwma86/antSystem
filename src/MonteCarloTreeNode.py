import logging
import math
import random

class MCTSNode:
    def __init__(self, environment, parent, currentFoodSource, ongoingTour = list()):
        self.Environment = environment
        self.RunCount = 0
        self.AverageTrailLength = 0

        self.Parent = parent

        self.OngoingTour = ongoingTour
        self.VisitedFoodSources = set(ongoingTour)
        self.CurrentFoodSource = currentFoodSource
        self.ChildNodes = []
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
        rolloutVisitedFoodSources = set(self.VisitedFoodSources)

        # Navigate unvisited food sources along the trails with the strongest Pheromones
        # until all Food Sources have been visited.
        rolloutTour = list(self.OngoingTour)

        # Find the strongest unvisited pheromone trail from this point
        currentFoodSource = self.CurrentFoodSource
        nextFoodSource = self.find_strongest_unvisited_pheromone_trail(currentFoodSource, rolloutVisitedFoodSources)

        while nextFoodSource is not None:
            rolloutTour.append(nextFoodSource)
            rolloutVisitedFoodSources.add(nextFoodSource)

            currentFoodSource = nextFoodSource

            nextFoodSource = self.find_strongest_unvisited_pheromone_trail(currentFoodSource, rolloutVisitedFoodSources)

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
            totalLength += math.sqrt(self.Environment.find_trail_distance(tour[i].FoodSourceId, tour[i + 1].FoodSourceId))
        
        return totalLength

    def find_strongest_unvisited_pheromone_trail(self, currentFoodSource, visitedFoodSources):
        #Get the list of potential paths from the current food source
        potentialTrails = self.Environment.FoodSourceDistances[currentFoodSource]

        strongestPheromoneFoodSource = None
        strongestPheromoneScore = 0
        for trailTuple in potentialTrails:
            targetFoodSourceId = self.Environment.get_target_foodsourceId(currentFoodSource, trailTuple)
            targetFoodSource = self.Environment.FoodSourceDict[targetFoodSourceId]
            if targetFoodSource in visitedFoodSources:
                continue
            pheromoneScore = self.Environment.get_pheromone_score(currentFoodSource.FoodSourceId, targetFoodSourceId)
            if pheromoneScore > strongestPheromoneScore:
                strongestPheromoneFoodSource = targetFoodSource
                strongestPheromoneScore = pheromoneScore

        return strongestPheromoneFoodSource

    def pick_unvisited_child(self):
        unvisitedChildren = [i for i in self.ChildNodes if i.get_visit_count() == 0]

        logging.info(f'Node {self.CurrentFoodSource.FoodSourceId} has {len(self.ChildNodes)} child Nodes and {len(unvisitedChildren)} unvisited Child Nodes')

        # This is a terminal node. It has no children.
        if len(unvisitedChildren) == 0:
            logging.info(f'Node {self.CurrentFoodSource.FoodSourceId} has NO MORE CHILDREN')
            return None

        # Pick the unvisited child with the highest pheromone score
        strongestChild = None
        strongestChildPheromoneScore = 0
        for child in unvisitedChildren:
            if child.get_pheromone_score() > strongestChildPheromoneScore:
                strongestChild = child
                strongestChildPheromoneScore = child.get_pheromone_score()

        if strongestChild is None:
            strongestChild = unvisitedChildren[random.randrange(0, len(unvisitedChildren))]


        logging.info(f'The strongest child of {self.CurrentFoodSource.FoodSourceId} is {strongestChild.CurrentFoodSource.FoodSourceId}')
        return strongestChild

    def fully_expanded(self):
        return len([i for i in self.ChildNodes if i.get_visit_count() == 0])
        
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
            if foodSource not in self.VisitedFoodSources and foodSource != self.CurrentFoodSource:
                ongoingTour = list(self.OngoingTour)
                ongoingTour.append(foodSource)
                node = MCTSNode(self.Environment, self, foodSource, ongoingTour)
                self.ChildNodes.append(node)

    def simulate(self):
        pass

    def get_foodsource(self):
        return self.CurrentFoodSource

    def get_pheromone_score(self):
        return self.PheromoneScore

    def get_visit_count(self):
        return self.VisitCount
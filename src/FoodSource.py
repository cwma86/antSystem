import math

class FoodSource: 
    def __init__(self, foodSourceDataString):
        try:
            foodData = [i.strip() for i in foodSourceDataString.split(' ')]
            self.FoodSourceId = int(foodData[0])
            self.XPos = float(foodData[1])
            self.YPos = float(foodData[2])
        except:
            print(foodSourceDataString)

    def __hash__(self):
        return hash(self.FoodSourceId)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.XPos == other.XPos
            and self.YPos == other.YPos
            # and self.FoodSourceId == other.FoodSourceId
        )
    
    def __str__(self):
        return f"Food Source ID: {self.FoodSourceId}, X:{self.XPos}, Y:{self.YPos}"

class Trail:
    def __init__(self, foodSource1, foodSource2):
        if(foodSource1.FoodSourceId < foodSource2.FoodSourceId):
            self.BeginFoodSource = foodSource1
            self.EndFoodSource = foodSource2
        else:
            self.BeginFoodSource = foodSource2
            self.EndFoodSource = foodSource1

        self.DistanceSquared = (foodSource1.XPos - foodSource2.XPos) ** 2 + (foodSource1.YPos - foodSource2.YPos) ** 2

    def get_target_foodsource(self, currentFoodSource):
        if currentFoodSource == self.BeginFoodSource:
            return self.EndFoodSource
        elif currentFoodSource == self.EndFoodSource:
            return self.BeginFoodSource

        return None
    
    def __hash__(self):
        return hash((self.BeginFoodSource, self.EndFoodSource))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.BeginFoodSource == other.BeginFoodSource
            and self.EndFoodSource == other.EndFoodSource
        )

    def __lt__(self, other):
        return self.DistanceSquared < other.DistanceSquared

    def __le__(self, other):
        self.DistanceSquared <= other.DistanceSquared

    def __gt__(self, other):
        self.DistanceSquared > other.DistanceSquared

    def __ge__(self, other):
        self.DistanceSquared >= other.DistanceSquared
    
    def __str__(self):
        return f"Starting Food Source: {self.BeginFoodSource}, Ending Food Source:{self.EndFoodSource}, Dist: {self.Distance}"
    
    def __repr__(self):
        return f"Starting Food Source: {self.BeginFoodSource}, Ending Food Source:{self.EndFoodSource}, Dist: {self.Distance}"

    
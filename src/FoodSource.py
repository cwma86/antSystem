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

    
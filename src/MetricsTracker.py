class MetricsTracker:
    def __init__(self):
        self.cycles = []
        pass

    def addCycle(self,count, length):
        self.cycles.append(CycleData(count,length))

    def getCycle(self,i):
        return self.cycles[i]

    def getReport(self):
        print(" ")
        print("Run Summary:")
        print("Total Cycles: ",len(self.cycles))
        shortest = float('inf')
        cycleIteration = 0
        for i in range(0, len(self.cycles)):
            length = self.cycles[i].length
            if (length < shortest):
                shortest = length
                cycleIteration = i
            if i % 5 == 0:
                print("Cycle: ",i, " Length: ", length)
        print("Cycle",cycleIteration,"Shortest Length: ",shortest)


class CycleData:
    def __init__(self, cycleCount, fullCycleLength):
        self.cycleCount = cycleCount
        self.length = fullCycleLength